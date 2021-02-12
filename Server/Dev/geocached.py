from sql_classes import User, UserSession, Location, LogEntry
from sql_queries import get_location
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Caching with style'

@app.route("/single_location/<int:location_id>")
def location_api(location_id):
    location = get_location(location_id)
    return location

if __name__ == '__main__':
    # db.create_all()
    app.run()