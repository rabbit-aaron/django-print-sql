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
    print('{}\n'.format(sqlparse.format(statement, reindent=True, keyword_case='upper')))



original_execute_sql = SQLCompiler.execute_sql

@contextmanager
def print_sql(count_only=False):

    query_count = {'count': 0}

    @wraps(original_execute_sql)
    def execute_sql(self, *args, **kwargs):
        query_count['count'] += 1
        if not count_only:
            pprint_sql(self.as_sql())
        return original_execute_sql(self, *args, **kwargs)

    # monkey patching the SQLCompiler
    SQLCompiler.execute_sql = execute_sql

    yield  # execute code in the `with` statement
    
    # restore original execute_sql
    SQLCompiler.execute_sql = original_execute_sql

    print('!!! {num_of_queries} {query_word} executed\n'.format(
        num_of_queries=query_count['count'],
        query_word='query' if query_count['count'] == 1 else 'queries',
    ))
