import pika
import json


class RabbitMQClient:
    def __init__(self, host='localhost', port=5672):
        self.host = host
        self.port = port
        self.exchange_name = 'cars_events_exchange'
        self.queue_name = 'cars_events_queue'
        self.routing_key = 'car.event'
        self._setup_connection()

    def _setup_connection(self):
        """Установка соединения и объявление exchange и queue"""
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port)
        )
        self.channel = self.connection.channel()

        # Объявляем exchange (тип direct)
        self.channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type='direct',
            durable=True
        )

        # Объявляем очередь
        self.channel.queue_declare(
            queue=self.queue_name,
            durable=True
        )

        # Привязываем очередь к exchange
        self.channel.queue_bind(
            exchange=self.exchange_name,
            queue=self.queue_name,
            routing_key=self.routing_key
        )

    def publish_event(self, event_type, car_data):
        """Публикация события в RabbitMQ"""
        event = {
            'eventType': event_type,
            'car': car_data
        }

        message_body = json.dumps(event, ensure_ascii=False)

        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message_body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Сохранять сообщения на диске
                content_type='application/json'
            )
        )
        print(f"[x] Отправлено событие: {event_type}")

    def close(self):
        """Закрытие соединения"""
        self.connection.close()