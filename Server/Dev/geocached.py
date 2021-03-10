from sql_classes import User, UserSession, Location, LogEntry
from sqlalchemy.exc import IntegrityError
import json
from flask import Flask, request

app = Flask(__name__)
from sql_link import sql_link

db_location = 'sqlite:///test.db'

sql_link = sql_link(db_location)


# sql_link.create_db_link()

# https://stackoverflow.com/questions/34009296/using-sqlalchemy-session-from-flask-raises-sqlite-objects-created-in-a-thread-c


@app.route('/')
def hello_world():
    return 'Caching with style'


@app.route("/get_single_location/")
def get_location():
    location_id = request.args.get('id')
    if location_id:
        location = sql_link.get_location(location_id)
        return location
    else:
        return "no location id"


@app.route("/get_location_list/")
def get_location_list():
    return sql_link.list_location_ids()


@app.route("/get_single_user/")
def get_user():
    user_id = request.args.get('id')
    if user_id:
        user = sql_link.get_user(user_id)
        return user
    else:
        return "no user id"


@app.route("/add_single_user/")
def add_user():
    # TODO: password should not be passed as GET, should be a POST?
    new_user = {'id': request.args.get('id'),
                'password': request.args.get('pw')}
    try:
        sql_link.add_user(new_user)
        return "success"
    except IntegrityError:
        return "user already exists"
    finally:
        return "failed to add"


@app.route("/add_location/")
def add_location():
    new_location = {"id": request.args.get("id"),
                    "name": request.args.get("name"),
                    "x_coord": request.args.get("x_coord"),
                    "y_coord": request.args.get("y_coord"),
                    "description": request.args.get("description")}
    try:
        sql_link.add_location(new_location)
        return "success"
    except IntegrityError:
        return "location already exists"
    finally:
        return "failed to add"


if __name__ == '__main__':
    app.run()
