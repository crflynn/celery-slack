"""Setup script."""
import io
from os import path
from setuptools import setup


here = path.abspath(path.dirname(__file__))

# io.open for py27
with io.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

about = {}
with open(path.join(here, 'celery_slack', '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System :: Logging',
        'Topic :: System :: Monitoring',
    ],
    keywords='celery slack',
    packages=['celery_slack'],
    install_requires=[
        'celery',
        'requests',
        'ephem',
    ],
    include_package_data=True,
)
