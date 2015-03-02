import os
from datetime import datetime

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static as static_helper
from django.utils.translation import activate as dj_activate, get_language

from feincms.module.medialibrary.models import MediaFile
from feincms.templatetags.feincms_tags import feincms_render_region
from jingo import register
from jinja2 import Markup
from sorl.thumbnail import get_thumbnail

from masterfirefoxos.base.models import Locale, Page


static = register.function(static_helper)


@register.function
def render_region(feincms_page, region, request):
    return Markup(feincms_render_region(None, feincms_page, region, request))


@register.function
def current_year():
    return datetime.now().strftime('%Y')


@register.function
def activate(language):
    dj_activate(language)
    return ''


@register.function
def slug_to_version(slug):
    return slug.replace('-', '.')


@register.function
def active_version(request):
    slug = request.path.split('/')[2]
    return slug_to_version(slug)


@register.function
def get_image_url(img, geometry=None, locale=None):
    if not locale:
        locale = get_language()
    url = img.file.url

    basename = os.path.basename(img.file.name).rsplit('.')[0]

    query = MediaFile.objects.filter(
        file__startswith='medialibrary/' + basename + '.',
        categories__title=locale)

    if query.exists():
        img = query.first()
        url = img.file.url

    if geometry:
        img = get_thumbnail(img.file, geometry, quality=90)
        url = img.url

    # AWS S3 urls contain AWS_ACCESS_KEY_ID, Expiration and other
    # params. We don't need them.
    return url.split('?')[0]


@register.function
def include_pontoon(request):
    return request.get_host() == getattr(settings, 'LOCALIZATION_HOST', None)


@register.function
def get_versions():
    return [(slug_to_version(p.slug), p.slug)
            for p in Page.objects.filter(parent__isnull=True)]


@register.function
def active_language_codes():
    return (Locale.objects
            .exclude(versions__isnull=True).values_list('code', flat=True))
