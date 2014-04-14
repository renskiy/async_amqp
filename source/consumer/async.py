import gevent.monkey
import kombu
import time

gevent.monkey.patch_all()

dsn = 'amqp://async_rabbitmq:async_rabbitmq@localhost:5672/async_rabbitmq'

greenlets = {}


def do_work(body, message):
    time.sleep(1)  # some useful work
    print(body)
    message.ack()
    del greenlets[id(gevent.getcurrent())]


def on_message(body, message):
    greenlet = gevent.spawn(do_work, body, message)
    greenlets[id(greenlet)] = greenlet


def main():
    try:
        with kombu.Connection(dsn) as connection:
            queues = (kombu.Queue(name='mail'), )
            with connection.Consumer(queues=queues, callbacks=(on_message, )):
                while True:
                    connection.drain_events()
    except KeyboardInterrupt:
        gevent.joinall(greenlets.values())


if __name__ == '__main__':
    main()
