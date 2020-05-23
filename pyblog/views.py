from django.conf import settings
from django.db.models import Prefetch
from django.http import JsonResponse
from django.views.generic import ListView, ArchiveIndexView
from django.views.generic.detail import DetailView

from comment.forms import get_comment_form, post_comment_form
from comment.models import Comment
from . import models


class PostListView(ListView):
    allow_empty = False
    queryset = models.Post.objects.filter(is_published=True).only('title', 'slug', 'content', 'updated_time')
    ordering = "-created_time"
    paginate_by = 5


class Index(PostListView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        result = super(__class__, self).get_context_data(**kwargs)
        result['keywords'] = settings.INDEX_KEYWORDS
        result['description'] = settings.INDEX_DESCRIPTION
        return result


class TagListView(PostListView):
    template_name = 'tag.html'

    def get_queryset(self):
        return super(__class__, self).get_queryset().filter(tags__title=self.kwargs['title'])

    def get_context_data(self, **kwargs):
        result = super(__class__, self).get_context_data(**kwargs)
        result['tag'] = models.Tag.objects.get(title=self.kwargs['title'])
        return result


class PostDetailView(DetailView):
    model = models.Post
    allow_empty = False
    template_name = 'post_detail.html'

    def get_queryset(self):
        return super(__class__, self).get_queryset().prefetch_related(
            Prefetch('tags', queryset=models.Tag.objects.only('title')))

    def get_context_data(self, **kwargs):
        result = super(__class__, self).get_context_data(**kwargs)
        result['comments'] = Comment.get_comment_list(uid=self.object.uid)
        result['commentForm'] = get_comment_form(self.request)
        result['relatedPosts'] = models.Post.objects.filter(tags__in=result['post'].tags.all()).exclude(
            id=result['post'].id).distinct().order_by('-created_time').only('slug', 'title')[:10]
        return result

    def post(self, request, *args, **kwargs):
        result = post_comment_form(request, self.get_object().uid)
        if self.request.is_ajax():
            return JsonResponse(result)
        else:
            return self.get(request, *args, **kwargs)


class ArchiveView(ArchiveIndexView):
    model = models.Post
    allow_empty = False
    date_field = 'created_time'
    date_list_period = 'month'
    template_name = 'archive.html'

    def get_queryset(self):
        return super(__class__, self).get_queryset().values('title', 'slug', 'created_time')
