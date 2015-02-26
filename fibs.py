
import numpy
from celery import Celery
import time
from decimal import Decimal

celery_app = Celery('fibs', backend='amqp', broker='amqp://guest@localhost//')


@celery_app.task
def crappy_fib(num):
    return str(do_crappy_fib(num))


def do_crappy_fib(num):
    if num < 2:
        return num
    if num > 30:
        time.sleep(15)
        return numpy_fib(num)
    return do_crappy_fib(num - 2) + do_crappy_fib(num - 1)


@celery_app.task
def numpy_fib(num):
    return str((numpy.uint64(numpy.matrix([[1, 1], [1, 0]]) ** (num-1))[0,0]))