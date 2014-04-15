import kombu
import logging
import time

dsn = 'amqp://async_rabbitmq:async_rabbitmq@localhost:5672/async_rabbitmq'

logging.basicConfig(level='DEBUG')


def do_work(body, message):
    time.sleep(1)  # some useful work
    print(body)
    message.ack()


def on_message(body, message):
    do_work(body, message)


def main():
    try:
        with kombu.Connection(dsn) as connection:
            queue = kombu.Queue(name='mail')
            with connection.Consumer(
                queues=(queue, ),
                callbacks=(on_message, ),
                auto_declare=False,
            ):
                while True:
                    connection.drain_events()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
