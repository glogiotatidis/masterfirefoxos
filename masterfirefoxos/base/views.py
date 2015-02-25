import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect

from .models import Locale, Page


def home_redirect(request):
    try:
        locale = Locale.objects.get(code=request.LANGUAGE_CODE)
    except ObjectDoesNotExist:
        try:
            locale = Locale.objects.get(code='en')
        except ObjectDoesNotExist:
            locale = None

    if locale and locale.latest_version:
        return HttpResponseRedirect(
            '/{}/{}/'.format(locale.code, locale.latest_version.slug))

    return HttpResponse('Setup Locales in /admin first')


def all_pages(request):
    pages = {}
    for p in Page.objects.filter(active=True):
        pages[p.slug] = [
            '/{}{}'.format(locale, p.get_navigation_url())
            for locale in settings.LANGUAGE_NAMES.keys()]
    return HttpResponse(json.dumps(pages))
