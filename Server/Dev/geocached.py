from sqlalchemy.exc import IntegrityError
import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_location = 'sqlite:///test.db'
app.config["SQLALCHEMY_DATABASE_URI"] = db_location
# from sql_link import sql_link
#
#
# sql_link = sql_link(db_location)

db = SQLAlchemy(app)

# https://stackoverflow.com/questions/34009296/using-sqlalchemy-session-from-flask-raises-sqlite-objects-created-in-a-thread-c


Base = db.Model


class User(Base):
    __tablename__ = 'user'

    id = db.Column(db.String(250), primary_key=True)
    password = db.Column(db.String(250), nullable=False)
    # some_new_field = db.Column(db.String(250),nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserSession(Base):
    __tablename__ = 'usersession'

    id = db.Column(db.String(250), db.ForeignKey('user.id'), primary_key=True)
    session_key = db.Column(db.String(250), nullable=False)
    valid_through = db.Column(db.DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Location(Base):
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    obscured_url = db.Column(db.String(250))
    clear_url = db.Column(db.String(250))
    x_coord = db.Column(db.String(20))
    y_coord = db.Column(db.String(20))
    description = db.Column(db.String(250), nullable=True)
    log_entries = db.relationship("LogEntry")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class LogEntry(Base):
    __tablename__ = "logentry"

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer,db.ForeignKey('location.id'),nullable=False)
    user_id = db.Column(db.String(250), db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime)
    text = db.Column(db.String(250))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def db_get_location(location_id: int):
    result = db.session.query(Location).filter_by(id=location_id).first()
    db.session.close()
    if result:
        return result.as_dict()
    else:
        return {}

def db_add_location(location_json: json):
    new_location = Location()
    new_location = set_columns_from_json(new_location, location_json)
    db.session.add(new_location)
    db.session.commit()
    db.session.close()

def db_list_location_ids():
    result = [instance.id for instance in db.session.query(Location.id)]
    db.session.close()
    return ",".join([str(x) for x in result])

def db_get_user(user_id: str):
    result = db.session.query(User).filter_by(id=user_id).first()
    db.session.close()
    if result:
        return result.as_dict()
    else:
        return {}

def db_add_user(json_data: json):
    new_obj = User()
    new_obj = set_columns_from_json(new_obj, json_data)
    db.session.add(new_obj)
    db.session.commit()
    db.session.close()


def set_columns_from_json(new_object: object, input_json: json):
    attribute_list = [attrname for attrname in dir(new_object) if attrname[:1] != "_"]
    # print(attribute_list)
    for single_key in input_json.keys():
        if single_key in attribute_list:
            setattr(new_object, single_key, input_json[single_key])
    return new_object



@app.route('/')
def hello_world():
    return 'Caching with style'


@app.route("/get_single_location/")
def get_location():
    location_id = request.args.get('id')
    if location_id:
        location = db_get_location(location_id)
        return location
    else:
        return "no location id"


@app.route("/get_location_list/")
def get_location_list():
    return db_list_location_ids()


@app.route("/get_single_user/")
def get_user():
    user_id = request.args.get('id')
    if user_id:
        user = db_get_user(user_id)
        return user
    else:
        return "no user id"


@app.route("/add_single_user/")
def add_user():
    # TODO: password should not be passed as GET, should be a POST?
    new_user = {'id': request.args.get('id'),
                'password': request.args.get('pw')}
    try:
        db_add_user(new_user)
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
        db_add_location(new_location)
        return "success"
    except IntegrityError:
        return "location already exists"
    finally:
        return "failed to add"


if __name__ == '__main__':
    app.run()
