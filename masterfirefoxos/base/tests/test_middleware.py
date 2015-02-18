from unittest.mock import Mock, patch

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser, User

from masterfirefoxos.base.middleware import NonExistentLocaleRedirectionMiddleware


middleware = NonExistentLocaleRedirectionMiddleware()


def test_user_authenticated():
    request = RequestFactory().get('/en/foo-bar')
    request.user = User()
    assert middleware.process_request(request) is None


def test_path_starts_with_en():
    request = RequestFactory().get('/en/foo-bar')
    request.user = AnonymousUser()
    assert middleware.process_request(request) is None


def test_path_starts_with_admin():
    request = RequestFactory().get('/admin/foo')
    request.user = AnonymousUser()
    assert middleware.process_request(request) is None


def test_locale_for_version_exists():
    request = RequestFactory().get('/xx/version-90')
    request.user = AnonymousUser()
    with patch('masterfirefoxos.base.middleware.Locale') as LocaleMock:
        with patch('masterfirefoxos.base.middleware.Page') as PageMock:
            PageMock.objects.filter().exists.return_value = True
            locale_mock = Mock()
            LocaleMock.objects.get.return_value = locale_mock
            locale_mock.versions.filter().exists.return_value = True
            assert middleware.process_request(request) is None


def test_locale_for_version_does_not_exist():
    request = RequestFactory().get('/xx/version-100t/demo-tips')
    request.user = AnonymousUser()
    with patch('masterfirefoxos.base.middleware.Locale') as LocaleMock:
        with patch('masterfirefoxos.base.middleware.Page') as PageMock:
            PageMock.objects.filter().exists.return_value = True
            locale_mock = Mock()
            locale_mock.latest_version = None
            LocaleMock.objects.get.return_value = locale_mock
            locale_mock.versions.filter().exists.return_value = False
            response = middleware.process_request(request)
    assert isinstance(response, HttpResponseRedirect)
    assert response.url == '/en/version-100t/demo-tips?from-lang=xx'


def test_with_nonexistant_version():
    request = RequestFactory().get('/xx/version-does-not-exist/demo-tips')
    request.user = AnonymousUser()

    with patch('masterfirefoxos.base.middleware.Locale') as LocaleMock:
        with patch('masterfirefoxos.base.middleware.Page') as PageMock:
            PageMock.objects.filter().exists.return_value = False
            locale_mock = Mock()
            LocaleMock.objects.get.return_value = locale_mock
            locale_mock.versions.filter().exists.return_value = False
            assert middleware.process_request(request) is None


def test_with_nonexistant_locale():
    request = RequestFactory().get('/xx/version-100t/demo-tips')
    request.user = AnonymousUser()
    with patch('masterfirefoxos.base.middleware.Locale') as LocaleMock:
        with patch('masterfirefoxos.base.middleware.Page') as PageMock:
            PageMock.objects.filter().exists.return_value = True
            LocaleMock.objects.get.side_effect = [ObjectDoesNotExist()]
            assert middleware.process_request(request) is None


def test_request_path_breakdown_failure():
    request = RequestFactory().get('/')
    request.user = AnonymousUser()
    assert middleware.process_request(request) is None
