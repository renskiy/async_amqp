import kombu
import logging

dsn = 'amqp://async_rabbitmq:async_rabbitmq@localhost:5672/async_rabbitmq'

logging.basicConfig(level='DEBUG')


def send_messages(number_of_messages=1):
    with kombu.Connection(dsn) as connection:
        exchange = kombu.Exchange(name='tasks')
        producer = connection.Producer(exchange=exchange, auto_declare=False)
        for message_number in range(number_of_messages):
            routing_key = 'task.mail.{}'.format(message_number)
            message = 'This is message #{}'.format(message_number)
            producer.publish(message, routing_key=routing_key)
    print('Successfully sent {} messages'.format(number_of_messages))


if __name__ == '__main__':
    send_messages(10)
