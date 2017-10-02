from django.conf import settings

def info(request):
      re = {
          'siteTitle': settings.SITE_TITLE,
          'siteSummary': settings.SITE_SUMMARY
          
      }
      return re