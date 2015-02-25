import requests
import pytest


acceptance = pytest.mark.acceptance


def assert_ok(url):
    response = requests.get(url)
    assert response.status_code == 200, '{} for {}'.format(
        response.status_code, url)


def get_all_versions(base_url, urls):
    for url in urls:
        assert_ok('{}{}'.format(base_url, url))


@acceptance
def test_introduction(base_url, urls):
    get_all_versions(base_url, urls['introduction'])


@acceptance
def test_demo_tips(base_url, urls):
    get_all_versions(base_url, urls['demo-tips'])


@acceptance
def test_customer_guide(base_url, urls):
    get_all_versions(base_url, urls['customer-guide'])


@acceptance
def test_key_features(base_url, urls):
    get_all_versions(base_url, urls['key-features'])


@acceptance
def test_faq(base_url, urls):
    get_all_versions(base_url, urls['frequently-asked-questions'])


@acceptance
def test_about(base_url, urls):
    get_all_versions(base_url, urls['about'])


@acceptance
def test_quiz(base_url, urls):
    get_all_versions(base_url, urls['take-the-challenge'])


@acceptance
def test_which_version(base_url, urls):
    get_all_versions(base_url, urls['which-version'])


@acceptance
def test_other_pages(base_url, urls):
    pages = list((set(urls.keys()) -
             set(['which-version', 'take-the-challenge', 'the-firefox-mission',
                  'frequently-asked-questions', 'key-features', 'customer-guide',
                  'demo-tips', 'introduction'])))
    for page in pages:
        get_all_versions(base_url, urls[page])
