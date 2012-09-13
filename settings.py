#!/usr/bin/env python
# coding: utf-8

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   General
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SITENAME = "kalnitsky's way"
SITEURL = 'http://www.kalnitsky.org'
AUTHOR = 'Igor Kalnitsky'

THEME = 'themes/nifty'
MYOPENID = 'kalnitsky'
GOOGLE_ANALYTICS = 'UA-9629423-12'
YANDEX_METRIKA = '9491932'

TIMEZONE = "Europe/Kiev"
LOCALE = ('ru_RU.utf8', 'en_US.utf8')
DEFAULT_LANG = 'ru'
DATE_FORMATS = {
    'ru': ('ru_RU.utf8', '%d %b %Y'),
    'en': ('en_US.utf8', '%d %b %Y'),
}

WEBASSETS = True
TAG_CLOUD_STEPS = 100
DEFAULT_PAGINATION = False
DIRECT_TEMPLATES = ('index', 'tags')
PLUGINS = ['pelican.plugins.sitemap', ]

ARTICLE_DIR = 'posts'
PAGE_DIR = 'pages'
STATIC_PATHS = ['images', ]
FILES_TO_COPY = (
    ('extra/robots.txt', 'robots.txt'),
    ('extra/favicon.ico', 'favicon.ico'),
    ('extra/ikalnitsky-pub.asc', 'ikalnitsky-pub.asc'),
)

SITEMAP = {
    'generate': ['articles', 'pages'],
    'format': 'xml',
    'changefreqs': {
        'articles': None,
        'pages': None,
    },
    'priorities': {
        'articles': None,
        'pages': None,
    }
}

NAVIGATION_BAR = (
    ('Projects', '/projects/'),
)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Utils
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def is_localhost():
    '''
    NOTE: The ``.localhost`` file should be
          exists in a localhost machine.
    '''
    import os
    import inspect

    root = os.path.dirname(inspect.getfile(inspect.currentframe()))
    if os.path.exists(os.path.join(root, '.localhost')):
        return True
    return False


def get_lang_by_code(lang_code):
    '''
    Translate ``Language Code`` to ``Language Name``.
    Used in ``nifty`` templates.
    '''
    from babel import Locale
    return Locale(lang_code).display_name


if is_localhost():
    SITEURL = 'http://localhost:8000'
LANGUAGE_NAME = get_lang_by_code


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   URL
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RELATIVE_URLS = False

ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
ARTICLE_LANG_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/{lang}/'
ARTICLE_LANG_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/{lang}/index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
PAGE_LANG_URL = '{slug}/{lang}/'
PAGE_LANG_SAVE_AS = '{slug}/{lang}/index.html'

TAG_URL = 'tags/{slug}/'
TAG_SAVE_AS = 'tags/{slug}/index.html'
TAGS_URL = 'tags/'
TAGS_SAVE_AS = 'tags/index.html'

FEED_DOMAIN = SITEURL
FEED_ATOM = 'feed/index.xml'
TRANSLATION_FEED = 'feed/%s/index.xml'
TAG_FEED_ATOM = 'tags/%s/feed/index.xml'
CATEGORY_FEED_ATOM = None

# NOT GENERATE SOME PAGES
AUTHOR_SAVE_AS = False
ARCHIVES_SAVE_AS = False
CATEGORY_SAVE_AS = False
CATEGORIES_SAVE_AS = False
CATEGORY_FEED = False
