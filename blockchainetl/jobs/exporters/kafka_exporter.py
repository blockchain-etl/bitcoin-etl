import collections
import json
import logging
import os
import socket

from confluent_kafka import Producer

from blockchainetl.jobs.exporters.converters.composite_item_converter import CompositeItemConverter
from blockchainetl.jobs.exporters.bitcoin_flatten import flatten_transformation


class KafkaItemExporter:

    def __init__(self, output, item_type_to_topic_mapping, converters=()):
        self.item_type_to_topic_mapping = item_type_to_topic_mapping
        self.converter = CompositeItemConverter(converters)
        self.connection_url = self.get_connection_url(output)
        # print(self.connection_url)
        conf = {
            "bootstrap.servers": os.getenv("CONFLUENT_BROKER"),
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "client.id": socket.gethostname(),
            "message.max.bytes": 5242880,
            "sasl.username": os.getenv("CONFLUENT_USERNAME"),
            "sasl.password": os.getenv("CONFLUENT_PASSWORD")
        }

        self.producer = Producer(conf)

    def get_connection_url(self, output):
        try:
            return output.split('/')[1]
        except KeyError:
            raise Exception('Invalid kafka output param, It should be in format of "kafka/127.0.0.1:9092"')

    def open(self):
        pass

    def acked(err, msg):
        if err is not None:
            logging.error("Failed to deliver message: %s: %s" % (str(msg), str(err)))
        else:
            logging.debug("Message produced: %s" % (str(msg)))     

    def export_items(self, items):
        for item in items:
            item_type = item.get('type')
            if item_type is not None and item_type in self.item_type_to_topic_mapping:
                if(item_type == "transaction"):
                    transformed_data = flatten_transformation(item)
                    for data in transformed_data:
                        self.export_item(data,item_type)
                else:
                    self.export_item(item,item_type)
            else:
                logging.warning('Topic for item type "{}" is not configured.'.format(item_type))

    def export_item(self, item, item_type):
        data = json.dumps(item).encode('utf-8')
        message_future = self.write_to_kafka(value=data,
                                             topic=self.item_type_to_topic_mapping[item_type])
        
        return message_future


    def write_to_kafka(self, value: str, topic: str):
        try:
            self.producer.produce(topic,key="0x0000",value=value, callback=self.acked)
        except BufferError:
            self.logging.error('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                             len(self.producer))
        self.producer.poll(0)
  

    def convert_items(self, items):
        for item in items:
            yield self.converter.convert_item(item)

    def close(self):
        pass


def group_by_item_type(items):
    result = collections.defaultdict(list)
    for item in items:
        result[item.get('type')].append(item)

    return result