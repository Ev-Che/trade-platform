from trade.services.kafka_service.kafka_producer import Producer


class KafkaMessagingService:
    TOPIC = 'test'

    def send_message_to_kafka(self, emails: list) -> None:
        Producer().send_message(topic=self.TOPIC, emails=emails)
