from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Caching with style'


if __name__ == '__main__':
    # db.create_all()
    app.run()