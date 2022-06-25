import os
import requests
import logging

import flask
#from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace import config_integration
from opencensus.trace.tracer import Tracer
from opencensus.trace.samplers import AlwaysOnSampler
from ocpubsubexporter import PubsubExporter

config_integration.trace_integrations(["requests"])

app = flask.Flask(__name__)

tracer = Tracer(sampler=AlwaysOnSampler(), exporter=PubsubExporter(logger=app.logger))
#middleware = FlaskMiddleware(app, excludelist_paths=["_ah/health"])


random_company_url = os.getenv("RANDOM_COMPANY_URI")


@app.route("/api/random/company")
def company():
    app.logger.debug("getting random company")
    with tracer.span(name="randomcompany") as span1:
        if not random_company_url:
            return "random company request URL not configured", 500
        res = None
        with span1.span(name="fetchrandomcompany"):
            res = requests.get(random_company_url)
            if res.status_code != 200:
                app.logger.warn("bad status code %i", res.status_code)
                return "error fetching random company", res.status_code
        try:
            return res.json()
        except requests.exceptions.JSONDecodeError | AttributeError as e:
            app.logger.exception(e)
            return (
                "unexpected response fetching random company %s, %s"
                % (random_company_url, res.headers.get("Content-Type")),
                500,
            )


@app.route("/")
def root():
    return """
            <a href="/api/random/company">/api/company/random</a>
        """

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
else:
    app.debug = True
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.debug("logging configured")
