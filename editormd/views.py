from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from editormd.models import Image
from pyblog.models import Article


@csrf_exempt
def upload(request):
    if request.user.is_superuser:
        photo = request.FILES.get('editormd-image-file', None)
        json = {'success': 0, }
        if photo:
            try:
                img = Image(img=photo, rel=Article.objects.get(id=(request.META.get('HTTP_REFERER').split('/')[-3])))
            except IndexError:
                return HttpResponseBadRequest()
            img.save()
            json = {
                'success': 1,
                'url': img.img.url,
            }
        return JsonResponse(json)
    return HttpResponseForbidden()
