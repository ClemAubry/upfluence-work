from flask import Flask, abort
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)
cache = SimpleCache()


@app.route('/processing/<int:input_number>', methods=['PUT', ])
def processing(input_number):
    if input_number < 3:
        return str(1)
    a, b = 1, 1
    while input_number > 2:
        input_number -= 1
        a, b = b, a+b
    return str(b)


@app.route('/processing/cache/<int:input_number>', methods=['PUT', ])
def processing_cache(input_number):

    if cache.get('number-1') is None:
        cache.set('number-1', 1)
    if cache.get('number-2') is None:
        cache.set('number-2', 1)

    i, cache_number = input_number, cache.get('number-{}'.format(input_number))

    # On descend 2 par 2 pour diviser par 2 le nombre de get, au lieu de décroître un par un
    while i > 2 and cache_number is None:
        i, cache_number = i-2, cache.get('number-{}'.format((i-2)))

    # On instancie a et b
    if cache.get('number-{}'.format(i+1)) is not None:
        a, b = cache.get('number-{}'.format(i)), cache.get('number-{}'.format((i+1)))
        i += 1
    else:
        a, b = cache.get('number-{}'.format((i-1))), cache.get('number-{}'.format(i))

    # Calcul et mise en cache
    while i < input_number:
        a, b = b, a+b
        i += 1
        cache.set('number-{}'.format(i), b)

    return str(b)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['HEAD', 'GET', 'POST', 'OPTIONS', 'DELETE', 'PUT'])
def index(path):
    abort(404, 'Wrong path')
