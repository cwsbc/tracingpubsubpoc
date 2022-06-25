FROM python:2.7-slim
WORKDIR /build
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY setup.py ./
COPY src/ src/
RUN python setup.py install
WORKDIR /app
ENV FLASK_APP otps
ENV RANDOM_COMPANY_URI https://random-data-api.com/api/company/random_company
ENV PUBSUB_EMULATOR_HOST=pubsub:8085
ENV PUBSUB_PROJECT_ID=bluecore-tracepubsub-poc
ENV PUBSUB_TOPIC=bluecoregaetraces
CMD gunicorn --log-level=debug -w 2 -b 0.0.0.0:5555 --access-logfile - --capture-output 'otps:app'
#CMD flask run --host=0.0.0.0
