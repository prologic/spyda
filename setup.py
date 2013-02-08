#!/usr/bin/env python

import os
from glob import glob
from distutils.util import convert_path

from setuptools import setup


def find_packages(where=".", exclude=()):
    """Borrowed directly from setuptools"""

    out = []
    stack = [(convert_path(where), "")]
    while stack:
        where, prefix = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if ("." not in name and os.path.isdir(fn) and
                    os.path.isfile(os.path.join(fn, "__init__.py"))):
                out.append(prefix + name)
                stack.append((fn, prefix + name + "."))

    from fnmatch import fnmatchcase
    for pat in list(exclude) + ["ez_setup"]:
        out = [item for item in out if not fnmatchcase(item, pat)]

    return out

path = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(path, "README.rst")).read()
    RELEASE = open(os.path.join(path, "RELEASE.rst")).read()
except IOError:
    README = RELEASE = ""

setup(
    name="spyda",
    version="0.0.2dev",
    description="Python Spider Tool(s) and Library",
    long_description="%s\n\n%s" % (README, RELEASE),
    author="James Mills",
    author_email="James Mills, j dot mills at griffith dot edu dot au",
    url="TBA",
    download_url="TBA",
    classifiers=[],
    license="TBA",
    keywords="Python Spider Web Crawling and Extraction Tool and Library",
    platforms="POSIX",
    packages=find_packages("."),
    scripts=glob("scripts/*"),
    install_requires=[
        "url",
        "lxml",
        "nltk",
        "cssselect",
        "restclient",
        "BeautifulSoup"
    ],
    entry_points={
        "console_scripts": [
            "crawl=spyda.crawler:main",
            "extract=spyda.extractor:main"
            "match=spyda.matcher:main"
        ]
    },
    zip_safe=False,
    test_suite="tests.main.runtests",
)
