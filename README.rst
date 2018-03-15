django-print-sql
================

django-print-sql is an easy-to-use SQL debug tool for Django developers to print SQL statements


What's new
----------

**2018.3.6**

* Added a decorator
* It now prints how long it takes each query to execute, as well as the total time elapsed

Requirements
------------

You need to have django installed (obviously).

I've tried it on Django 1.11.11 and 2.0.3.

If sqlparse is installed, the SQL statement wil be formatted.

Install
-------

From pip, run::

    $ pip install --upgrade django-print-sql

Consider using the ``--user`` option_.

.. _option: https://pip.pypa.io/en/latest/user_guide/#user-installs

From the repository, run::

  python setup.py install

to install django-print-sql on your system.

django-print-sql is compatible with Python 2.7 and Python 3 (>= 3.3) (hopefully :D).

Install sqlparse to pretty print the statements::

  $ pip install --upgrade sqlparse

Usage
-----
Example 1. Use as context manager::

  from django_print_sql import print_sql
  
  # set `count_only` to `True` will print the number of executed SQL statements only
  with print_sql(count_only=False):

    # write the code you want to analyze in here,
    # e.g. some complex foreign key lookup,
    # or analyzing a DRF serializer's performance

    for user in User.objects.all()[:10]:
        user.groups.first()

Example 2. Use as decorator::

  from django_print_sql import print_sql_decorator


    @print_sql_decorator(count_only=False)  # this works on class-based views as well
    def get(request):
        # your view code here

Links
-----

Project Page
  https://github.com/rabbit-aaron/django-print-sql

django-print-sql is licensed under the MIT license.

Parts of the readme are based on sqlparse's readme file.
sqlparse: https://github.com/andialbrecht/sqlparse
