from django import forms
from .models import Comment


class GuestForm(forms.ModelForm):
    nikename = forms.CharField(label='昵称',max_length=30)
    email = forms.EmailField(label='邮箱',max_length=50)
    url = forms.URLField(label='网站',required=False)
    to = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['nikename', 'email', 'url', 'content', 'allow_email']


class AuthenticatedForm(forms.ModelForm):
    to = forms.IntegerField(widget = forms.HiddenInput,required=False)

    class Meta:
        model = Comment
        fields = ['content', 'allow_email']


def get_comment_form(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            form = AuthenticatedForm(request.POST)
        else:
            form = GuestForm(request.POST)
    else:
        if request.user.is_authenticated():
            form = AuthenticatedForm()
        else:
            form = GuestForm()
    return form


def post_comment_form(request,fk):
    '''
    提交评论表单
    '''
    form = get_comment_form(request)
    if form.is_valid():
            result = {'status': 1}

            new_comment = form.save(commit=False)
            new_comment.article = fk
            new_comment.ip      = request.META.get('HTTP_X_FORWARDED_FOR',request.META.get('REMOTE_ADDR',None))
            new_comment.user    = request.user if request.user.is_authenticated() else None
            new_comment.ua      = request.META.get('HTTP_USER_AGENT',None)
            #判断是否有上级评论字段
            if form.cleaned_data['to'] != None:
                to_comment =  Comment.objects.filter(id=form.cleaned_data['to'],article=fk,is_pub=True).first()
                #判断上级评论是否存在
                if to_comment != None:
                    if to_comment.parent == None:
                        new_comment.parent = to_comment
                    else:
                        new_comment.parent = to_comment.parent
                        new_comment.at     = to_comment
                    #上级评论是否允许邮件通知
                    if to_comment.allow_email:
                        #发送邮件
                        new_comment.send_email([to_comment.get_email(),], request.path)
                else:
                    return {'status': 0}

            new_comment.save()
    else:
        result = {
            'status': 0,
            'errors': form.errors,
        }
    return result