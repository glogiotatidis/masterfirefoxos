from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

from .helpers import slug_to_version
from .models import Locale, Page


class NonExistentLocaleRedirectionMiddleware(object):
    """Redirect to the 'en' version of a page if translation does not exist.

    This middleware redirects requests to pages with locale other than
    'en' to their 'en' version. The map of available locales and
    documentation versions is maintained in
    settings.VERSIONS_LOCALE_MAP.

    If the user is authenticated, i.e. is staff, they don't get
    redirected and they can view the requested page. This will be
    useful to verify translations before releasing them.

    """

    def process_request(self, request):
        if ((hasattr(request, 'user') and request.user.is_authenticated())
            or request.path.startswith('/admin')):
            return

        if request.path.startswith('/en/'):
            return

        url_breakdown = request.path.split('/')
        try:
            version_slug = url_breakdown[2]
            locale = url_breakdown[1]
        except IndexError:
            # Normally we would never need handle this exception
            # because this middleware comes after LocaleMiddleware,
            # which because it adds locale in the url it makes the
            # url_breakdown to have a least 3 parts when split. But
            # let's play it safe and just return if that ever happens.
            return

        try:
            locale_obj = Locale.objects.get(code=locale)
        except ObjectDoesNotExist:
            locale_obj = None

        # If locale exists, version exists but version in locale does not exist.
        if (locale_obj and not locale_obj.versions.filter(slug=version_slug).exists()
            and Page.objects.filter(parent__isnull=True, slug=version_slug).exists()):

            url_breakdown[1] = 'en'
            new_path = '/'.join(url_breakdown)
            params = request.GET.copy()
            params['from-lang'] = locale
            if locale_obj:
                latest = locale_obj.latest_version
                if latest:
                    params['latest-version'] = slug_to_version(latest.slug)
            return HttpResponseRedirect(
                '?'.join([new_path, params.urlencode()]))

        return
