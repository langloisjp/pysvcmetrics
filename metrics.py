"""
Module to provide easy access to submitting metrics.

Similar to logging, code can always emit metrics, but those
metrics might not go anywhere without a consumer, e.g.
statsdclient.

Call configure() to setup a consumer.

Dependencies:
- statsdclient

"""

import statsdclient
import logging

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8125


class NullClient(object): # pragma: no cover
    """An instrumentation 'null' client"""
    def timeit(self, _metric, func, *args, **kwargs):
        """Dummy timeit"""
        return func(*args, **kwargs)

    def count(self, *args, **kwargs):
        """Dummy count"""
        pass

    def timing(self, *args):
        """Dummy timing"""
        pass

    def gauge(self, *args):
        """Dummy gauge"""
        pass


_client = NullClient()

def configure(host=DEFAULT_HOST, port=DEFAULT_PORT, prefix=''):
    """
    >>> configure()
    >>> configure('localhost', 8125, 'mymetrics')
    """
    global _client
    logging.info("Reconfiguring metrics: {}:{}/{}".format(host, port, prefix))
    _client = statsdclient.StatsdClient(host, port, prefix)

def timing(metric, value):
    """
    >>> timing("metric", 33)
    """
    _client.timing(metric, value)

def gauge(metric, value):
    """
    >>> gauge("gauge", 23)
    """
    _client.gauge(metric, value)

def count(metric, value=1, sample_rate=1):
    """
    >>> count("metric")
    >>> count("metric", 3)
    >>> count("metric", -2)
    """
    _client.count(metric, value, sample_rate)

def timeit(metric, func, *args, **kwargs):
    """
    >>> import time
    >>> timeit("metric", time.sleep, 0.1)
    >>> resetclient()
    >>> timeit("metric", time.sleep, 0.1)
    """
    return _client.timeit(metric, func, *args, **kwargs)

def resetclient():
    """
    Reset client to None

    >>> resetclient()
    """
    global _client
    _client = NullClient()

def timed(prefix=None):
    """
    Decorator to time execution of function.
    Metric name is function name (as given under f.__name__).
    Optionally provide a prefix (without the '.').

    >>> @timed()
    ... def f():
    ...     print('ok')
    ...
    >>> f()
    ok
    >>> @timed(prefix='mymetrics')
    ... def g():
    ...     print('ok')
    ...
    >>> g()
    ok
    """
    def decorator(func):
        """wrap func so it is timed"""
        metricname = func.__name__

        if prefix:
            metricname = prefix + '.' + metricname

        def wrapped(*args, **kwargs):
            """wrapped function"""
            return timeit(metricname, func, *args, **kwargs)
        return wrapped

    return decorator

def time_methods(obj, methods, prefix=None):
    """
    Patch obj so calls to given methods are timed

    >>> class C(object):
    ...     def m1(self):
    ...         return 'ok'
    ...
    ...     def m2(self, arg):
    ...         return arg
    ...
    >>> c = C()
    >>> time_methods(c, ['m1', 'm2'])
    >>> c.m1()
    'ok'
    >>> c.m2('ok')
    'ok'
    >>> c = C()
    >>> time_methods(c, ['m1'], 'mymetrics')
    """
    if prefix:
        prefix = prefix + '.'
    else:
        prefix = ''

    for method in methods:
        current_method = getattr(obj, method)
        new_method = timed(prefix)(current_method)
        setattr(obj, method, new_method)
