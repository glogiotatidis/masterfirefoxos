from unittest.mock import Mock, patch

from django.core.exceptions import ObjectDoesNotExist
from django.test import RequestFactory

from .. import views


def test_home_redirect_de():
    request = RequestFactory().get('/de/')
    request.LANGUAGE_CODE = 'de'  # normally added by LocaleMiddleware
    with patch('masterfirefoxos.base.views.Locale') as LocaleMock:
        locale_mock = Mock()
        locale_mock.code = 'de'
        locale_mock.latest_version.slug = ('1-1')
        LocaleMock.objects.get.return_value = locale_mock
        response = views.home_redirect(request)
    assert response.status_code == 302
    assert response['location'] == '/de/1-1/'


def test_home_redirect_english_default():
    request = RequestFactory().get('/de/')
    request.LANGUAGE_CODE = 'de'  # normally added by LocaleMiddleware
    with patch('masterfirefoxos.base.views.Locale') as LocaleMock:
        locale_mock = Mock()
        locale_mock.code = 'en'
        locale_mock.latest_version.slug = ('1-1')
        LocaleMock.objects.get.side_effect = [
            ObjectDoesNotExist(),
            locale_mock
        ]
        response = views.home_redirect(request)
    assert response.status_code == 302
    assert response['location'] == '/en/1-1/'


def test_home_redirect_no_locales_set():
    request = RequestFactory().get('/en/')
    request.LANGUAGE_CODE = 'en'  # normally added by LocaleMiddleware
    with patch('masterfirefoxos.base.views.Locale') as LocaleMock:
        LocaleMock.objects.get.side_effect = [
            ObjectDoesNotExist(),
            ObjectDoesNotExist()
        ]
        response = views.home_redirect(request)
    assert response.status_code == 200
