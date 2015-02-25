from django.core.urlresolvers import reverse

import pytest
import requests


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
def urls(base_url):
    return requests.get('{}{}'.format(base_url, reverse('all_pages'))).json()
