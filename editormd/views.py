from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from editormd.models import Image


@csrf_exempt
def upload(request):
    if request.user.is_superuser:
        photo = request.FILES.get('editormd-image-file', None)
        json = {'success': 0, }
        if photo:
            img = Image(img=photo)
            img.save()
            json = {
                'success': 1,
                'url': img.img.url,
            }
        return JsonResponse(json)
    return HttpResponseForbidden()
