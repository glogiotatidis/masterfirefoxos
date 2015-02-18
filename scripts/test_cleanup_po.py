from unittest.mock import Mock, patch

from django.core.exceptions import ObjectDoesNotExist

from cleanup_po import code_string, get_versions_for_locale, valid_version


def test_code_string():
    assert code_string([('foo', 2), ('bar', 3)]) is True
    assert code_string([('foo', 3), ('db-strings.txt', 10)]) is True
    assert code_string([('db-strings.txt', 10)]) is False


def test_valid_version():
    comment = 'FooBar\nPage path: /1-3T/foo/bar\nLalo'
    assert valid_version(comment, ['1-1', '1-3T']) is True
    assert valid_version(comment, ['2-0', '1-3']) is False


def test_get_versions_for_locale():
    def _test(locale, versions, pending_versions):
        with patch('cleanup_po.Locale') as LocaleMock:
            locale_mock = Mock()
            locale_mock.versions.values_list.return_value = versions
            locale_mock.pending_versions.values_list.return_value = pending_versions
            LocaleMock.objects.get.return_value = locale_mock
            assert set(get_versions_for_locale(locale)) == set(versions + pending_versions)
    _test('xx', ['version-90'], [])
    _test('en', ['version-90', 'version-100t'], [])
    _test('foo', [], ['version-100t'])
    _test('bar', ['version-90'], ['version-100t'])


def test_get_versions_for_non_existent_locale():
    with patch('cleanup_po.Locale') as LocaleMock:
        LocaleMock.objects.get.side_effect = [ObjectDoesNotExist]
        assert get_versions_for_locale('xx') == []
