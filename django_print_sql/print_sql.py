import time
from django.db.models.sql.compiler import SQLCompiler
from functools import wraps
from contextlib import contextmanager
import traceback
import codecs

import logging
logger = logging.getLogger(__name__)

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
    logger.debug(sqlparse.format(statement, reindent=True, keyword_case='upper'))


original_execute_sql = SQLCompiler.execute_sql


@contextmanager
def print_sql(count_only=False):

    shared_var = {'count': 0, 'total_time': 0, 'first_time' : 0}

    @wraps(original_execute_sql)
    def execute_sql(self, *args, **kwargs):
        shared_var['count'] += 1
        time_begin = time.time()
        if shared_var['first_time'] == 0:
            shared_var['first_time'] = time_begin
        ret = original_execute_sql(self, *args, **kwargs)
        time_elapsed = time.time() - time_begin
        shared_var['total_time'] += time_elapsed
        if not count_only:
            pprint_sql(self.as_sql())
            logger.debug('[{time_begin:.5f}s since start, time elapsed: {time:.2f}ms]\n\n'.format(
                time_begin=time_begin-shared_var['first_time'], time=time_elapsed * 1000))
        return ret

    # monkey patching the SQLCompiler
    SQLCompiler.execute_sql = execute_sql

    yield  # execute code in the `with` statement
    
    # restore original execute_sql
    SQLCompiler.execute_sql = original_execute_sql

    logger.debug('[{num_of_queries} {query_word} executed, total time elapsed {time:.2f}ms]\n'.format(
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


@contextmanager
def print_sql_to_file(log_file_path, trace=False, trace_base_str=None):
    """
        Because the SQL and traceback log can be large and/or sensitive,
        we save it to a file instead of logger.debug.

        Setting trace_base_str to the start of the absolute path
        to the python source files prints the traceback info
        corresponding to the point where the DB query is made.
    """

    shared_var = {'count': 0, 'total_time': 0, 'first_time' : 0}

    logf = codecs.open(log_file_path, 'w', encoding='utf-8')

    @wraps(original_execute_sql)
    def execute_sql(self, *args, **kwargs):
        shared_var['count'] += 1
        time_begin = time.time()
        if shared_var['first_time'] == 0:
            shared_var['first_time'] = time_begin
        ret = original_execute_sql(self, *args, **kwargs)
        time_elapsed = time.time() - time_begin
        shared_var['total_time'] += time_elapsed

        if trace:
            trb = traceback.extract_stack()
            trb_i = len(trb) - 1
            while trb_i >=0:
                if trace_base_str is not None:
                    # when set and the source file path starts with some string
                    if trb[trb_i][0].startswith(trace_base_str):
                        logf.write( '%s, %s, %s, %s\n' % trb[trb_i] )
                else:
                    logf.write( '%s, %s, %s, %s\n' % trb[trb_i] )
                trb_i -= 1
        
        sql_query = self.as_sql()
        sql_statement = sql_query[0] % sql_query[1]
        sql_statement = (sqlparse.format(sql_statement, reindent=True, keyword_case='upper'))
        logf.write(sql_statement)
        logf.write("\n")

        logf.write('[{time_begin:.5f}s since start, time elapsed: {time:.2f}ms]\n\n'.format(
            time_begin=time_begin-shared_var['first_time'], time=time_elapsed * 1000))

        return ret

    # monkey patching the SQLCompiler
    SQLCompiler.execute_sql = execute_sql

    yield  # execute code in the `with` statement
    
    # restore original execute_sql
    SQLCompiler.execute_sql = original_execute_sql

    logf.write('[{num_of_queries} {query_word} executed, total time elapsed {time:.2f}ms]\n\n'.format(
        num_of_queries=shared_var['count'],
        query_word='query' if shared_var['count'] == 1 else 'queries',
        time=shared_var['total_time'] * 1000
    ))

    logf.close()

