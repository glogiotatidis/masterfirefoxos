from unittest.mock import Mock

from feincms.module.medialibrary.models import MediaFile
from sorl.thumbnail import ImageField


def MediaFileFactory(filename='filename.jpg', url='media_url'):
    media_file = MediaFile()
    media_file.file = Mock()
    media_file.file.name = filename
    media_file.file.url = url
    return media_file


def ImageFieldFactory(filename='filename.jpg', url='image_url'):
    image_file = ImageField()
    image_file.name = filename
    image_file.url = url
    return image_file
