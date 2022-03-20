from flask import Flask, abort, redirect

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

if __name__ == '__main__':
    app.run()
