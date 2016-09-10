from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>welcome to Naaru</h1>'


@app.route('/login')
def login():
    return '<h1>login to Naaru</h1>'


if __name__ == '__main__':
    app.run(port=4546)
