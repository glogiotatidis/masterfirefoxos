import pytest

from masterfirefoxos.base.helpers import active_language_codes
from masterfirefoxos.base.models import Page


def pytest_addoption(parser):
    parser.addoption('--acceptance', action="store_true",
                     help="run acceptance tests")
    parser.addoption('--baseurl', action='store', dest='base_url',
                     default='http://localhost:8000', metavar='url',
                     help='base url test against for acceptance tests')


def pytest_runtest_setup(item):
    if 'acceptance' in item.keywords and not item.config.getoption(
            "--acceptance"):
        pytest.skip("need --acceptance option to run")


@pytest.fixture
def base_url(request):
    return request.config.getoption('--baseurl')


@pytest.fixture
def base_urls(base_url):
    return ['/'.join([base_url, locale, slug, ''])
            for slug in Page.objects.filter(parent__isnull=True).values_list('slug', flat=True)
            for locale in active_language_codes()]
