
from flask import Flask

from fibs import (
    celery_app,
    crappy_fib,
    numpy_fib,
)

flask_app = Flask("lightning-rabbit")

results = {}


@flask_app.route('/crappy_fib/<int:num>')
def crappy_fib_route(num):
    result = crappy_fib.delay(num)
    results[result.id] = result
    return result.id


@flask_app.route('/numpy_fib/<int:num>')
def numpy_fib_route(num):
    result = numpy_fib.delay(num)
    results[result.id] = result
    return result.id


if __name__ == '__main__':
    flask_app.run(host="localhost", port=5000, debug=True)