
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
        item['result'] = retrieve_task(item['obj'])
    return render_template("show_results.html", results=results, tasks=celery_app.tasks)


def add_to_results(num, obj):
    global results
    results.append({
        "num": num,
        "obj": obj,
        "result": retrieve_task(obj)
    })


def retrieve_task(task):
    if task.ready():
        return task.get(timeout=1)
    else:
        return "not ready"


if __name__ == '__main__':
    flask_app.run(host="localhost", port=5000, debug=True)