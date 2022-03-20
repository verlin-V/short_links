import hashlib

from flask import Flask, abort, redirect, request

app = Flask(__name__)

FAKE_TABLE = {
    'hgrdy43': 'https://google.com/',
}

@app.route('/<hash>')
def redirect_to_saved_link(hash):
    if hash in FAKE_TABLE:
        return redirect(FAKE_TABLE[hash], code=301)
    else:
        return abort(404)


@app.route('/add', methods=['POST'])
def add_short_link():
    try:
        url = request.json['url']
    except KeyError:
        return '"url" was expected in body', 400

    hash_url = hashlib.md5(url.encode('UTF-8')).hexdigest()
    FAKE_TABLE[hash_url] = url
    return f'{request.url_root}{hash_url}'


if __name__ == '__main__':
    app.run()
