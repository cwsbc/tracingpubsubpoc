# GAE OpenCensus to PubSub to OpenTelemetry PoC


## Components
* python - the python directory hosts a python 2.7 flask app which creates simple traces using OpenCensus and publishes them to pubsub using a horribly hacked together and shamefully written opencensus exporter.
* relay - a basic go server to pull spans off of pubsub and send them to an opentelemetry collector
* resources - config file for the opentelemetry collector

## Running the PoC

    > docker-compose build
    > docker-compose up

Using curl or a web browser, hit `http://localhost:5555/api/random/company`

Observe the spans being logged in the logs.

Since you really want to see the traces instead of text... sigh.

I guess I'll install Jaeger for you. Needy. http://localhost:16686/search


