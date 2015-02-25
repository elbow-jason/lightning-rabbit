
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
)

from fibs import (
    celery_app,
    crappy_fib,
    numpy_fib,
)

flask_app = Flask("lightning-rabbit")

results = []


@flask_app.route('/crappy_fib/<int:num>')
def crappy_fib_route(num):
    obj = crappy_fib.delay(num)
    add_to_results(num, obj)
    return redirect(url_for('show_results'))


@flask_app.route('/numpy_fib/<int:num>')
def numpy_fib_route(num):
    obj = numpy_fib.delay(num)
    add_to_results(num, obj)
    return redirect(url_for('show_results'))


@flask_app.route('/show_results')
def show_results():
    for item in results:
        retrieve_task(item)
    return render_template("show_results.html", results=results, tasks=celery_app.tasks)


def add_to_results(num, obj):
    global results
    item = {"num": num, "obj": obj}
    retrieve_task(item)
    results.append(item)


def retrieve_task(item):
    if item['obj'].ready():
        result = item['obj'].get(timeout=1)
        print "result", result
        item['result'] = result
    else:
        item['result'] = "not ready"
    print item


def get_task_by_id(task_id):
    result = MyTask.AsyncResult(task_id)


if __name__ == '__main__':
    flask_app.run(host="localhost", port=5000, debug=True)