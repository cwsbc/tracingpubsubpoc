import os
import logging

from google.cloud import pubsub_v1

from opencensus.common.transports import sync, base
from opencensus.trace import base_exporter, span_data, execution_context
from opencensus.ext.jaeger.trace_exporter  import JaegerExporter
from opencensus.ext.jaeger.trace_exporter.gen.jaeger import jaeger, agent

from thrift.protocol import TBinaryProtocol, TCompactProtocol
from thrift.transport import TTransport, THttpClient


class PubsubExporter(base_exporter.Exporter):

    def __init__(self, logger=None):
        self.transport = sync.SyncTransport(self)
        #self.http_transport = THttpClient.THttpClient(uri_or_host="http://otel:14268")
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_name = "projects/%s/topics/%s" %(os.getenv("PUBSUB_PROJECT_ID"), os.getenv("PUBSUB_TOPIC"))
        self.jaeger = JaegerExporter()
        self.buffer = TTransport.TMemoryBuffer()
        self.client = agent.Client(iprot=TCompactProtocol.TCompactProtocol(trans=self.buffer))
        #self.client = jaeger.Client(iprot=TBinaryProtocol.TBinaryProtocol(trans=self.http_transport))
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger()


    def emit(self, span_data):
        data = None
        try:
            jaeger_spans = self.jaeger.translate_to_jaeger(span_data)
        except Exception as e:
            self.logger.exception("could not translate to jaeger %s", e)
            raise e
        try:
            batch = jaeger.Batch(spans=jaeger_spans, process=jaeger.Process(serviceName="pubsubpoc"))
        except Exception as e:
            self.logger.exception("could not create batch %s", e)
            raise e
        try:
            #  truncate and reset the position of BytesIO object
            self.buffer._buffer.truncate(0)
            self.buffer._buffer.seek(0)
            self.client.emitBatch(batch)
            #self.client.submitBatches([batch])
            #self.logger.debug("reponse code %d message %s", self.http_transport.code, self.http_transport.message)
        except Exception as e:
            self.logger.exception("client.emitBatch failed %s", e)
            raise e
        try:
            buff = self.buffer.getvalue()
            future = self.publisher.publish(self.topic_name, buff)
            future.add_done_callback(lambda x: self.logger.debug("message published") if not x.exception() else self.logger.exception("publish failed %s", x.exception(timeout=10)))
        except Exception as e:
            self.logger.exception("could not publish span %s", e)
            raise e


    def export(self, span_datas):
        self.transport.export(span_datas)

