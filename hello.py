from flask import Flask, abort
app = Flask(__name__)


@app.route('/processing/<int:input_number>', methods=['PUT', ])
def processing(input_number):
    if input_number < 3:
        return str(1)
    a, b = 1, 1
    while input_number > 2:
        input_number -= 1
        a, b = b, a+b
    return str(b)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['HEAD', 'GET', 'POST', 'OPTIONS', 'DELETE', 'PUT'])
def index(path):
    abort(404, 'Wrong path')
