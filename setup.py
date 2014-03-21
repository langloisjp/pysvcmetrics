from setuptools import setup

setup(name='pysvcmetrics',
      version='0.1',
      description='Utilities to send metrics to graphite via statsd',
      url='https://github.com/langloisjp/pysvcmetrics',
      author='Jean-Philippe Langlois',
      author_email='jpl@jplanglois.com',
      license='MIT',
      py_modules=['metrics', 'statsdclient'],
      zip_safe=True)
