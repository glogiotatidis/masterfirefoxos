from unittest.mock import Mock, patch

from sorl.thumbnail.images import ImageFile

from ..helpers import get_image_url


def test_get_image_url_geometry():
    with patch('masterfirefoxos.base.helpers.get_thumbnail') as get_thumbnail_mock:
        response = get_image_url(ImageFile('foo'), geometry='200')
    get_thumbnail_mock.called_with('foo', '200')


def test_get_image_url_localized_file_exists():
    with patch('masterfirefoxos.base.helpers.default_storage') as default_storage_mock:
        with patch('masterfirefoxos.base.helpers.ImageFile') as ImageFileMock:
            default_storage_mock.exists.return_value = True
            img_mock = Mock()
            img_mock.url = 'localized url'
            ImageFileMock.return_value = img_mock
            response = get_image_url(ImageFile('foo'), locale='el')
    assert response == 'localized url'


def test_get_image_url_localized_file_does_not_exist():
    with patch('masterfirefoxos.base.helpers.default_storage') as default_storage_mock:
        with patch('masterfirefoxos.base.helpers.ImageFile') as ImageFileMock:
            default_storage_mock.exists.return_value = False
            img_file = ImageFile('foo')
            response = get_image_url(img_file, locale='el')
    assert response == img_file.url
