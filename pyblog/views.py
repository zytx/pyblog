from django.http import JsonResponse

from django.views.generic  import TemplateView,ListView,ArchiveIndexView
from django.views.generic.base import ContextMixin
from django.views.generic.detail import DetailView
from django.db.models import Q,Count
from .models import Article,Category,Tag

from comment.forms import get_comment_form,post_comment_form
from comment.models import Comment
from authentication.forms import UserLoginForm,UserCreationForm
from collections import OrderedDict


# Create your views here.


class SiteAJAX(ContextMixin):
    allow_empty  = False #不允许空页面

    def get_context_data(self, **kwargs):
        re           = super(SiteAJAX,self).get_context_data(**kwargs)
        if( not self.request.is_ajax() ):
            re['siderbar'] = {
                    'categorys' : Category.objects.values('title','slug'),
                         'tags' : Tag.objects.values('title','slug'),
                          'hot' : Article.objects.filter(is_pub=True).annotate(Count('comment')).order_by('-comment__count','-pub_date').values('title','slug','comment__count')[:8]
            }
            re['checkboxAJAX'] = self.request.COOKIES.get('AJAX','1')
            re['loginForm'] = UserLoginForm()
            re['regForm'] = UserCreationForm()
        re['siteTitle'] = "Mr.Z's blog"
        return re


class ArticleList(SiteAJAX,ListView):
    queryset      = Article.objects.select_related('category').prefetch_related('tags').filter(is_pub=True)
    ordering      = "-pub_date"
    paginate_by   = 5


class Index(ArticleList):
    template_name = 'index.html'


class CategoryList(ArticleList):
    template_name = 'category.html'

    def get_queryset(self):
        return super(__class__,self).get_queryset().filter(category__slug=self.args[0])


class TagList(ArticleList):
    template_name = 'tag.html'

    def get_queryset(self):
        return super(__class__,self).get_queryset().filter(tags__slug=self.args[0])


class ArticleDetail(SiteAJAX,DetailView):
    model = Article
    template_name = 'article.html'

    def get_queryset(self):
        return super(__class__,self).get_queryset().select_related('category').prefetch_related('tags')

    def get_context_data(self,**kwargs):
        re  = super(__class__,self).get_context_data(**kwargs)
        comments = Comment.objects.select_related('user','parent','at__user').order_by('parent','date').filter(article=re['article'])

        re['comments'] = OrderedDict()
        for comment in comments:
            if comment.parent == None:
                re['comments'][comment.id] = {
                    'parent': comment,
                    'reply' : []
                }
            else:
                re['comments'][comment.parent.id]['reply'].append(comment)
        re['commentForm'] = get_comment_form(self.request)
        re['relatedArticles'] = Article.objects.filter(Q(category=re['article'].category) | Q(tags__in=re['article'].tags.all())).order_by('-pub_date').values('slug','title')[:10]
        return re

    def post(self, request, *args, **kwargs):
        result = post_comment_form(request,Article.objects.get(slug=kwargs['slug']))
        if self.request.is_ajax():
            return JsonResponse(result)
        else:
            return self.get(request, *args, **kwargs)


class Archive(SiteAJAX,ArchiveIndexView):
    model = Article
    date_field = 'pub_date'
    date_list_period = 'month'
    template_name = 'archive.html'
    def get_context_data(self, **kwargs):
        re               = super(__class__,self).get_context_data(**kwargs)
        return re