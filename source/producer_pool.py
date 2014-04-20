import kombu
from kombu.pools import connections
import logging

dsn = 'amqp://async_rabbitmq:async_rabbitmq@localhost:5672/async_rabbitmq'

connection = kombu.Connection(dsn)

logging.basicConfig(level='DEBUG')


def send_messages(number_of_messages=1):
    with connections[connection].acquire(block=True) as conn:
        exchange = kombu.Exchange(name='tasks')
        producer = conn.Producer(exchange=exchange, auto_declare=False)
        for message_number in range(number_of_messages):
            routing_key = 'task.mail.{}'.format(message_number)
            message = dict(
                subject='Message #{}'.format(message_number),
                message='This is message #{}'.format(message_number),
                from_email='no-reply@example.com',
                recipient_list=('user@example.com', ),
            )
            producer.publish(message, routing_key=routing_key)
    print('Successfully sent {} messages'.format(number_of_messages))


if __name__ == '__main__':
    send_messages(10)
