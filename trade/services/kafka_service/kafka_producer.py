import json

from kafka import KafkaProducer

from trade_platform.settings import env


class Producer:

    def __init__(self):
        self._producer = KafkaProducer(
            bootstrap_servers=[env('LOCAL_ADDRESS')],
            value_serializer=self.serializer
        )

    @staticmethod
    def serializer(message):
        return json.dumps(message).encode('utf-8')

    def send_message(self, topic, emails):
        return self._producer.send(topic=topic, value=emails)
