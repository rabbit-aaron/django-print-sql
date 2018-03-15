import time
from django.db.models.sql.compiler import SQLCompiler
from functools import wraps
from contextlib import contextmanager

try:
    import sqlparse
except ImportError:
    import warnings
    warnings.warn('`pip install sqlparse` to use the pretty print feature')

    class sqlparse(object):

        @staticmethod
        def format(statement, *args, **kwargs):
            return statement


def pprint_sql(query):
    statement = query[0] % query[1]
    print(sqlparse.format(statement, reindent=True, keyword_case='upper'))


original_execute_sql = SQLCompiler.execute_sql


@contextmanager
def print_sql(count_only=False):

    shared_var = {'count': 0, 'total_time': 0}

    @wraps(original_execute_sql)
    def execute_sql(self, *args, **kwargs):
        shared_var['count'] += 1
        time_begin = time.time()
        ret = original_execute_sql(self, *args, **kwargs)
        time_elapsed = time.time() - time_begin
        shared_var['total_time'] += time_elapsed
        if not count_only:
            pprint_sql(self.as_sql())
            print('[Time elapsed: {time:.2f}ms]\n'.format(time=time_elapsed * 1000))
        return ret

    # monkey patching the SQLCompiler
    SQLCompiler.execute_sql = execute_sql

    yield  # execute code in the `with` statement
    
    # restore original execute_sql
    SQLCompiler.execute_sql = original_execute_sql

    print('[{num_of_queries} {query_word} executed, total time elapsed {time:.2f}ms]\n'.format(
        num_of_queries=shared_var['count'],
        query_word='query' if shared_var['count'] == 1 else 'queries',
        time=shared_var['total_time'] * 1000
    ))


def print_sql_decorator(*args, **kwargs):
    def wrapper(func):
        @wraps(func)
        def wrapped(*fargs, **fkwargs):
            with print_sql(*args, **kwargs):
                return func(*fargs, **fkwargs)
        return wrapped
    return wrapper
