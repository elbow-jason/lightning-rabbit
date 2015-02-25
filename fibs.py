
import numpy
from celery import Celery

celery_app = Celery('fibs', backend='amqp', broker='amqp://guest@localhost//')


@celery_app.task
def crappy_fib(num):
    if num < 2:
        return num
    if num > 30:
        return numpy_fib(num)
    return crappy_fib(num - 2) + crappy_fib(num - 1)


@celery_app.task
def numpy_fib(num):
    if num > 90:
        return str(num) + " was too high and would wrap the integer."
    return (numpy.matrix([[1, 1], [1, 0]]) ** (num-1))[0,0]