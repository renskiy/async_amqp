import gevent.monkey
gevent.monkey.patch_all()

import gevent.lock
import kombu
import logging
import time


dsn = 'pyamqp://async_rabbitmq:async_rabbitmq@localhost:5672/async_rabbitmq'

greenlets = {}

logging.basicConfig(level='DEBUG')

semaphore = gevent.lock.Semaphore(5)


def async(fn):
    def _fn(*args, **kwargs):
        fn(*args, **kwargs)
        del greenlets[id(gevent.getcurrent())]
        semaphore.release()

    def spawn_greenlet(*args, **kwargs):
        greenlet = gevent.spawn(_fn, *args, **kwargs)
        greenlets[id(greenlet)] = greenlet

    return spawn_greenlet


@async
def on_message(body, message):
    time.sleep(1)  # some useful work
    print("body = {body}, delivery_info = {delivery_info}".format(
        body=body, delivery_info=message.delivery_info))
    message.ack()


def main():
    with kombu.Connection(dsn) as connection:
        try:
            queue = kombu.Queue(name='mail')
            with connection.Consumer(
                queues=(queue, ),
                callbacks=(on_message, ),
                auto_declare=False,
            ):
                while True:
                    semaphore.acquire() and connection.drain_events()
                    gevent.sleep()  # release execution cursor
        except KeyboardInterrupt:
            gevent.joinall(greenlets.values())


if __name__ == '__main__':
    main()
