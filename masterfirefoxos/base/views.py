from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import never_cache


def home_redirect(request):
    version = settings.LOCALE_LATEST_VERSION.get(request.LANGUAGE_CODE)
    if version:
        return HttpResponseRedirect(version['slug'] + '/')
    return HttpResponseRedirect(
        '/{}/{}/'.format('en', settings.LOCALE_LATEST_VERSION['en']['slug']))


@never_cache
def logged_in(request):
    if request.user.is_authenticated():
        return render(request, 'loggedinbanner.html')

    return HttpResponse('')
