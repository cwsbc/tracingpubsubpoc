#!/usr/bin/env python
from distutils.core import setup
import setuptools

setup(
    name="otps",
    version="0.0.1",
    description="OpenCensus to OpenTelemetry over PubSub POC",
    author="Chad Slater",
    author_email="chad.slater@bluecore.com",
    packages=["otps", "ocpubsubexporter"],
    package_dir={"": "src"},
    install_requires=[
        "flask<2.0",
        "markupsafe<2.0",
        "gunicorn<20.0",
        "opencensus-ext-flask",
        "requests<2.28.0",
        "certifi<2020.4.5.2",
        "packaging<21.0",
        "pyparsing<3.0.0",
        "cachetools<4.0",
        "google-cloud-pubsub<2.0",
        "grpcio<1.40",
        "google-api-core<2.0",
        "opencensus-ext-jaeger"
    ],
)
# [project]
# name = "otps"
# version = "0.0.1"
# authors = [
#   { name = "Chad Slater", email = "chad.slater@bluecore.com" },
# ]
# requires-python = ">=2.7,<3"
# dependencies = [
#   "Flask"
# ]

# [build-system]
# requires = ["setuptools"]
# build-backend = "setuptools.build_meta"
