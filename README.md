pysvcmetrics
============

Utilities to send metrics to graphite via statsd

- statsdclient.py: To send metrics to statsd
- metrics.py: a simpler interface to send metrics

# Run tests

Requires coverage. `pip install coverage`

	make test

# Build a source distribution file:

	make spkg

# Install

	make install

# Install for development (files are linked to so changes are live)

	python setup.py develop

