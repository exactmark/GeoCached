from sqlalchemy.exc import IntegrityError
import json
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import globals
import uuid
import time
import datetime

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'jpg'}

app = Flask(__name__)
db_location = 'sqlite:///test.db'
app.config["SQLALCHEMY_DATABASE_URI"] = db_location
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Limit to 16 megabyte uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

DEBUG_ERROR = "debug_error"

db = SQLAlchemy(app)

# https://stackoverflow.com/questions/34009296/using-sqlalchemy-session-from-flask-raises-sqlite-objects-created-in-a-thread-c


Base = db.Model


class User(Base):
    __tablename__ = 'user'

    id = db.Column(db.String(250), primary_key=True)
    password = db.Column(db.String(250), nullable=False)

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
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
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


def db_get_session(user_id: str):
    result = db.session.query(UserSession).filter_by(id=user_id).first()
    if result is None:
        return db_generate_session(user_id)
    result_dict = result.as_dict()

    # if result_dict["valid_through"] < datetime.now():
    #     db_delete_session(user_id)
    #     return db_generate_session(user_id)
    # else:
    #     return result.as_dict()["session_key"]
    return result_dict["session_key"]


def db_delete_session(user_id: str):
    target_record = db.session.query(UserSession).filter_by(id=user_id).first()
    if target_record is not None:
        db.session.delete(target_record)
        db.session.commit()


def db_delete_user(user_id: str):
    target_record = db.session.query(User).filter_by(id=user_id).first()
    if target_record is not None:
        db.session.delete(target_record)
        db.session.commit()


def db_generate_session(user_id: str):
    generated_uuid = str(uuid.uuid4())
    new_session = UserSession(id=user_id, session_key=generated_uuid)
    db.session.add(new_session)
    db.session.commit()
    db.session.close()
    return generated_uuid


def set_columns_from_json(new_object: object, input_json: json):
    attribute_list = [attrname for attrname in dir(new_object) if attrname[:1] != "_"]
    for single_key in input_json.keys():
        if single_key in attribute_list:
            setattr(new_object, single_key, input_json[single_key])
    return new_object


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


@app.route('/put_location_image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return {}


@app.route("/login/")
def login():
    proto_user = {'id': request.args.get('id'),
                  'password': request.args.get('pw')}
    user_entry = db_get_user(proto_user["id"])
    if "password" not in user_entry.keys():
        return {DEBUG_ERROR: "No user entry."}
    elif proto_user["password"] != user_entry["password"]:
        return {DEBUG_ERROR: "Bad password."}
    else:
        successful_login = True
        # TODO get session key here
        session_key = db_get_session(proto_user["id"])
        return {"session_key": session_key}


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
        return {DEBUG_ERROR: "No user found."}


@app.route("/add_single_user/")
def add_user():
    # TODO: password should not be passed as GET, should be a POST?
    new_user = {'id': request.args.get('id'),
                'password': request.args.get('pw')}
    existing = db_get_user(new_user["id"])
    if existing:
        return {DEBUG_ERROR: "User exists."}
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
