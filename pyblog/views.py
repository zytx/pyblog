from django.http import JsonResponse

from django.views.generic  import ListView,ArchiveIndexView
from django.views.generic.detail import DetailView
from django.db.models import Q,Count,Prefetch
from .models import Article,Category,Tag

from comment.forms import get_comment_form,post_comment_form
from comment.models import Comment
from authentication.forms import UserLoginForm,UserCreationForm

from django.conf import settings

# Create your views here.


class ArticleList(ListView):
    allow_empty   = False
    queryset      = Article.objects.select_related('category').filter(is_pub=True).only('title','slug','content','pub_date','category__title','category__slug')
    ordering      = "-pub_date"
    paginate_by   = 5


class Index(ArticleList):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        re                = super(__class__,self).get_context_data(**kwargs)
        re['keywords']    = settings.INDEX_KEYWORDS
        re['description'] = settings.INDEX_DESCRIPTION
        return re


class CategoryList(ArticleList):
    template_name = 'category.html'

    def get_queryset(self):
        return super(__class__,self).get_queryset().filter(category__slug=self.kwargs['slug'])

    def get_context_data(self,**kwargs):
        re             = super(__class__,self).get_context_data(**kwargs)
        re['category'] = Category.objects.get(slug=self.kwargs['slug'])
        return re


class TagList(ArticleList):
    template_name = 'tag.html'

    def get_queryset(self):
        return super(__class__,self).get_queryset().filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self,**kwargs):
        re  = super(__class__,self).get_context_data(**kwargs)
        re['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return re


class ArticleDetail(DetailView):
    model         = Article
    allow_empty   = False
    template_name = 'article.html'

    def get_queryset(self):
        return super(__class__,self).get_queryset().select_related('category').prefetch_related(Prefetch('tags', queryset=Tag.objects.only('title','slug'))).only('title','slug','keywords','desc','content','pub_date','category__title','category__slug')

    def get_context_data(self,**kwargs):
        re                    = super(__class__,self).get_context_data(**kwargs)
        re['comments']        = Comment.get_comment_list(article=self.object)
        re['commentForm']     = get_comment_form(self.request)
        re['relatedArticles'] = Article.objects.filter(Q(category=re['article'].category) | Q(tags__in=re['article'].tags.all())).exclude(slug=re['article'].slug).distinct().order_by('-pub_date').only('slug','title')[:10]
        return re

    def post(self, request, *args, **kwargs):
        result = post_comment_form(request,Article.objects.get(slug=kwargs['slug']))
        if self.request.is_ajax():
            return JsonResponse(result)
        else:
            return self.get(request, *args, **kwargs)


class Archive(ArchiveIndexView):
    model            = Article
    allow_empty      = False
    date_field       = 'pub_date'
    date_list_period = 'month'
    template_name    = 'archive.html'

    def get_queryset(self):
        return super(__class__,self).get_queryset().values('title','slug','pub_date')

    def get_context_data(self, **kwargs):
        re               = super(__class__,self).get_context_data(**kwargs)
        return re
