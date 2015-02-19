import os
import re
import shutil

from django.conf import settings

import polib


def code_string(occurrences):
    for occ in occurrences:
        if not occ[0].startswith('db-strings.txt'):
            return True
    return False


def valid_version(comment, versions):
    for version in versions:
        if re.search('Page path: /{}/'.format(re.escape(version)), comment):
            return True
    return False


def get_versions_for_locale(locale):
    versions = []
    for version, data in settings.VERSIONS_LOCALE_MAP.items():
        if (locale in data.get('locales', [])
            or locale in data.get('pending_locales', [])):
            versions.append(data['slug'])
    return versions


def cleanup_po(version, django_pofile, pofile):
    shutil.copy(django_pofile, pofile)
    po = polib.pofile(pofile)
    to_remove = []
    for entry in po:
        # Currently unused string, keep.
        if len(entry.occurrences) == 0:
            continue

        if version == 'common':
            if not code_string(entry.occurrences):
                to_remove.append(entry)
        else:
            if (code_string(entry.occurrences) or
                not valid_version(entry.comment, [version])):
                to_remove.append(entry)

    if to_remove:
        for entry in to_remove:
            po.remove(entry)

        po.save()


def run(*args):
    for locale, lang_name in list(settings.LANGUAGES) + [('templates', 'templates')]:
        if locale == 'templates':
            versions = ['1-1', '1-3T', '1-4', '2-0']
            pot_or_not = 't'
        else:
            versions = get_versions_for_locale(locale)
            pot_or_not = ''

        django_pofile = 'locale/{}/LC_MESSAGES/django.po{}'.format(locale, pot_or_not)
        if not os.path.exists(django_pofile):
            print('Cannot open po file {}'.format(django_pofile))
            continue

        for version in ['common'] + versions:
            pofile = 'locale/{}/LC_MESSAGES/{}.po{}'.format(locale, version, pot_or_not)
            cleanup_po(version, django_pofile, pofile)
