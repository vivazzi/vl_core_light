import os
from setuptools import setup, find_packages
from vl_core import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='vl_core',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    platforms=['OS Independent'],
    description='vl_core_light is vl_core (https://github.com/vivazzi/vl_core) without django-cms support',
    long_description=README,
    url='https://vuspace.pro/',
    download_url='https://bitbucket.org/vivazzi/vl_core_light/downloads/',
    author='Artem Maltsev',
    author_email='maltsev.artjom@gmail.com',
    keywords='django vl core',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', 
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django>=3.2.6',
        'django-file-resubmit>=0.5.2',
        'django-sass-processor>=1.0.1',
        'django-select2>=7.7.1',
        'unidecode>=1.3.0',
    ],
)
