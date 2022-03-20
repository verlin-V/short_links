from uuid import uuid4

from flask import Flask, abort, redirect, request

app = Flask(__name__)

FAKE_TABLE = {
    'hgrdy43': 'https://google.com/',
}


def _get_free_hash():
    while (hash_val := str(uuid4())[:8]) not in FAKE_TABLE:
        return hash_val


@app.route('/<hash_url>', methods=['GET', 'DELETE'])
def short_link(hash_url):
    if request.method == 'GET':
        if hash_url in FAKE_TABLE:
            return redirect(FAKE_TABLE[hash_url], code=301)
        else:
            return abort(404)
    elif request.method == 'DELETE':
        FAKE_TABLE.pop(hash_url, None)
        return '', 204


@app.route('/add', methods=['POST'])
def add_short_link():
    try:
        url = request.json['url']
    except KeyError:
        return '"url" was expected in body', 400

    hash_url = _get_free_hash()
    FAKE_TABLE[hash_url] = url
    return f'{request.url_root}{hash_url}'


if __name__ == '__main__':
    app.run()
