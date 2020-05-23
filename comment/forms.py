import json

import requests
from django import forms
from django.conf import settings

from .models import Comment


class AuthenticatedForm(forms.ModelForm):
    to = forms.IntegerField(widget=forms.HiddenInput, required=False)
    recaptcha_token = forms.CharField(show_hidden_initial=True, empty_value=False)

    class Meta:
        model = Comment
        fields = ['allow_email', 'recaptcha_token', 'content']

    def clean_content(self):
        token = self.cleaned_data.get('recaptcha_token')
        try:
            res = requests.post('https://recaptcha.net/recaptcha/api/siteverify', data={
                'secret': settings.RECAPTCHA_SECRET,
                'response': token
            }).json()
            if res.get('score', 0) < settings.RECAPTCHA_LEVEL:
                raise forms.ValidationError('Google reCAPTCHA said: "You are a robot"')
        except (requests.RequestException, json.JSONDecodeError):
            raise forms.ValidationError('reCAPTCHA API Error')
        return self.cleaned_data.get('content')


class GuestForm(AuthenticatedForm):
    nickname = forms.CharField(label='昵称', max_length=30)
    email = forms.EmailField(label='邮箱', max_length=50)
    url = forms.URLField(label='网站', required=False)

    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'url', 'allow_email', 'recaptcha_token', 'content']


def get_comment_form(request):
    form_class = AuthenticatedForm if request.user.is_authenticated else GuestForm
    return form_class(request.POST if request.method == 'POST' else None)


def post_comment_form(request, post_uid):
    """
    提交评论表单
    """
    form = get_comment_form(request)
    if form.is_valid():
        result = {'status': 1}

        new_comment = form.save(commit=False)
        new_comment.post_uid = post_uid
        new_comment.ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', None))
        new_comment.user = request.user if request.user.is_authenticated else None
        new_comment.ua = request.META.get('HTTP_USER_AGENT', None)
        # 判断是否有上级评论字段
        if form.cleaned_data['to']:
            to_comment = Comment.objects.filter(id=form.cleaned_data['to'], post_uid=post_uid, is_pub=True).first()
            # 判断上级评论是否存在
            if to_comment:
                if to_comment.parent:
                    new_comment.parent = to_comment.parent
                    new_comment.at = to_comment
                else:
                    new_comment.parent = to_comment
                # 上级评论是否允许邮件通知
                if to_comment.allow_email:
                    # 发送邮件
                    new_comment.send_email([to_comment.get_email(), ], request.path)
            else:
                return {'status': 0}

        new_comment.save()
    else:
        result = {
            'status': 0,
            'errors': form.errors,
        }
    return result
