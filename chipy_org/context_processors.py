from django.conf import settings

def site_preview(request):
    return {'SITE_PREVIEW': settings.SITE_PREVIEW}