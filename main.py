from uuid import uuid4

from dotenv import load_dotenv

load_dotenv('env/.env')

from utils import (
    hash_exists,
    get_link_by_hash,
    delete_link,
    add_short_link_to_database,
)
from flask import Flask, abort, redirect, request

app = Flask(__name__)


def _get_free_hash():
    while not hash_exists(hash_val := str(uuid4())[:8]):
        return hash_val


@app.route('/<hash_url>', methods=['GET', 'DELETE'])
def short_link(hash_url):
    if request.method == 'GET':
        if hash_exists(hash_url):
            return redirect(get_link_by_hash(hash_url), code=301)
        else:
            return abort(404)
    elif request.method == 'DELETE':
        delete_link(hash_url)
        return '', 204


@app.route('/add', methods=['POST'])
def add_short_link():
    try:
        url = request.json['url']
    except KeyError:
        return '"url" was expected in body', 400

    hash_url = _get_free_hash()
    add_short_link_to_database(url, hash_url)
    return f'{request.url_root}{hash_url}'


if __name__ == '__main__':
    app.run()
