# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='django-print-sql',  # Required
    version='2018.3.6',  # Required
    description='django_print_sql is an easy-to-use SQL debug tool for Django developers to print SQL statements',  # Required
    long_description=long_description,  # Optional
    url='https://github.com/rabbit-aaron/django-print-sql',  # Optional
    author='Aaron Zhang',  # Optional
    author_email='rabbit.aaron@gmail.com',
    classifiers=[  # Optional
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='django sql debug',  # Optional
    packages=find_packages(),  # Required
)
