import gevent.monkey
import gevent.lock
import kombu
import logging
import time

gevent.monkey.patch_all()

dsn = 'pyamqp://async_rabbitmq:async_rabbitmq@localhost:5672/async_rabbitmq'

greenlets = {}

logging.basicConfig(level='DEBUG')

semaphore = gevent.lock.Semaphore(5)


def do_work(body, message):
    time.sleep(1)  # some useful work
    print("body = {body}, delivery_info = {delivery_info}".format(
        body=body, delivery_info=message.delivery_info))
    message.ack()
    semaphore.release()
    del greenlets[id(gevent.getcurrent())]


def on_message(body, message):
    greenlet = gevent.spawn(do_work, body, message)
    greenlets[id(greenlet)] = greenlet


def main():
    try:
        with kombu.Connection(dsn) as connection:
            queue = kombu.Queue(name='mail')
            with connection.Consumer(
                queues=(queue, ),
                callbacks=(on_message, ),
                auto_declare=False,
                accept=('json', ),
            ):
                while True:
                    semaphore.acquire() and connection.drain_events()
    except KeyboardInterrupt:
        gevent.joinall(greenlets.values())


if __name__ == '__main__':
    main()
