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
import auth
from PIL import Image
from functools import wraps

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'jpg'}

app = Flask(__name__)
db_location = 'sqlite:///test.db'
app.config["SQLALCHEMY_DATABASE_URI"] = db_location
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config.update(
    TESTING=True,
    SECRET_KEY=auth.SECRET_KEY
)
# Limit to 16 megabyte uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

DEBUG_ERROR = "debug_error"
DEBUG_MESSAGE = "debug_message"
REQUIRE_SESSION_KEY = False

db = SQLAlchemy(app)

# https://stackoverflow.com/questions/34009296/using-sqlalchemy-session-from-flask-raises-sqlite-objects-created-in-a-thread-c


# **************
# MODELS START
# **************

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


# **************
# DB START
# **************


def db_get_location(location_id: int):
    result = db.session.query(Location).filter_by(id=location_id).first()
    db.session.close()
    if result:
        return result.as_dict()
    else:
        return None


def db_get_location_by_name(location_name: str):
    result = db.session.query(Location).filter_by(name=location_name).first()
    print(result)
    db.session.close()
    if result:
        return result.as_dict()
    else:
        return None


def db_location_is_duplicate(location_dict):
    # return False
    if db_get_location_by_name(location_dict["name"]):
        return True
    return False


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
        result_dict = result.as_dict()
        return result_dict
    else:
        return None


def db_add_user(json_data: json):
    new_obj = User()
    new_obj = set_columns_from_json(new_obj, json_data)
    db.session.add(new_obj)
    db.session.commit()
    db.session.close()


def db_get_new_session(user_id: str):
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


def db_get_session_owner(session_key):
    result = db.session.query(UserSession).filter_by(session_key=session_key).first()
    if result is None:
        return None
    else:
        return result.as_dict()["id"]


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
    return '.' in filename and get_extension(filename) in ALLOWED_EXTENSIONS


def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


def process_uploaded_image(new_filename):
    # using https://stackoverflow.com/questions/47143332/how-to-pixelate-a-square-image-to-256-big-pixels-with-python
    for x in [16, 32, 64]:
        img = Image.open(new_filename)
        # Resize smoothly down to 16x16 pixels
        imgSmall = img.resize((x, x), resample=Image.BILINEAR)
        result = imgSmall.resize(img.size, Image.NEAREST)
        no_extension = ".".join(new_filename.split(".")[:-1])
        result.save(no_extension + "_sub_" + str(x) + "." + get_extension(new_filename))


# **************
# DECORATORS START
# **************


def require_session_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not REQUIRE_SESSION_KEY:
            return func(*args, **kwargs)
        session_key = None
        if request.method == 'POST':
            session_key = request.form.get('session_key')
        else:
            session_key = request.args.get('session_key')
        if not session_key:
            return {DEBUG_ERROR: "no session key"}
        elif not db_get_session_owner(session_key):
            return {DEBUG_ERROR: "session key not found"}
        print(db_get_session_owner(session_key))
        return func(*args, **kwargs)

    return wrapper


# **************
# ROUTES START
# **************


@app.route('/')
def hello_world():
    return 'Caching with style'


@app.route("/get_location_list/")
@require_session_key
def get_location_list():
    """Gets a list of locations currently in the db.

    Args:
        None

    Returns:
        string: a comma separated list of id numbers
    """
    return db_list_location_ids()


@app.route("/get_single_location/")
@require_session_key
def get_location():
    """Gets json for single location

    Args:
    GET:
        id (int): The index to retrieve

    Returns:
        json: location information
    """
    location_id = request.args.get('id')
    if location_id:
        location = db_get_location(location_id)
        if location:
            return location
        else:
            return {DEBUG_ERROR: "location not found"}
    else:
        return {DEBUG_ERROR: "no location id"}





@app.route('/put_location_image', methods=['POST'])
@require_session_key
def upload_main_location_image():
    """Uploads the main image for a location and does some processing.
    The location must exist in the db.

    Args:
    POST:
        loc_id (int): The index to retrieve
        or
        loc_name (str): the Name as per the location table

    Returns:
        json: success/failure
    """
    loc_id = request.form.get('loc_id')
    if not loc_id:
        loc_name = request.form.get('loc_name')
        if loc_name:
            loc_id = (db_get_location_by_name(loc_name))["id"]
            loc_id = str(loc_id)
    if loc_id is None:
        return {DEBUG_ERROR: "Required key not provided"}
    if 'file' not in request.files:
        return {DEBUG_ERROR: "No file part."}
    file = request.files['file']
    if file.filename == '':
        return {DEBUG_ERROR: "No selected file"}
    print(file.filename)
    if file and allowed_file(file.filename):
        # if we were trusting the user filename, we'd need this
        # filename = secure_filename(file.filename)
        new_filename = loc_id + "." + get_extension(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(file_path)
        process_uploaded_image(file_path)
        return {DEBUG_MESSAGE: "File upload successful"}





@app.route("/add_location/", methods=['POST'])
@require_session_key
def add_location():
    """Allows creation of new location.
    Will assign the next integer as id.
    Probably not parallel safe

    Args:
    POST:
        name (str): The location name. Currently being checked for uniqueness
        x_coord (str): Latitude
        y_coord (str): Longitude
        description (str): A short description

    Returns:
        json: success/failure
    """
    last_loc_id = db_list_location_ids().split(",")[-1]
    if last_loc_id is not '':
        proto_id = str(int(last_loc_id) + 1)
    else:
        proto_id = '0'
    # not multi process safe
    new_location = {"id": proto_id,
                    "name": request.form.get("name"),
                    "x_coord": request.form.get("x_coord"),
                    "y_coord": request.form.get("y_coord"),
                    "description": request.form.get("description")}

    try:
        if db_location_is_duplicate(new_location):
            return {DEBUG_ERROR: "Location is duplicate"}
        db_add_location(new_location)
        return {DEBUG_MESSAGE: "success", "id": proto_id}
    except IntegrityError:
        return {DEBUG_ERROR: "failed to add"}

@app.route("/login/", methods=['POST'])
def login():
    """Allows login

    Args:
    POST:
        id (str): User name
        pw (str): Password

    Returns:
        json: failure message or session_key
    """
    proto_user = {'id': request.form.get('id'),
                  'password': request.form.get('pw')}
    user_entry = db_get_user(proto_user["id"])
    if not user_entry:
        return {DEBUG_MESSAGE: "No user entry."}
    if "password" not in user_entry.keys():
        return {DEBUG_ERROR: "No user entry."}
    elif proto_user["password"] != user_entry["password"]:
        return {DEBUG_ERROR: "Bad password."}
    # TODO add session timeout?
    else:
        successful_login = True
        session_key = db_get_new_session(proto_user["id"])
        return {"session_key": session_key}


@app.route("/get_single_user/")
@require_session_key
def get_user():
    """Check if a user exists

    Args:
    GET:
        id (str): User name

    Returns:
        json: failure message or id
    """
    user_id = request.args.get('id')
    user = db_get_user(user_id)
    if user:
        user["password"] = ""
        return user
    else:
        return {DEBUG_ERROR: "No user found."}


@app.route("/add_single_user/", methods=['POST'])
@require_session_key
def add_user():
    """Creates user in db

    Args:
    POST:
        id (str): User name
        pw (str): password

    Returns:
        json: failure message or id
    """
    if request.method == 'POST':
        id = request.form.get('id')
        pw = request.form.get('pw')
        new_user = {'id': id,
                    'password': pw}
        existing = db_get_user(new_user["id"])
        if existing:
            return {DEBUG_ERROR: "User exists."}
        try:
            db_add_user(new_user)
            return {DEBUG_MESSAGE: "User added"}
        except IntegrityError:
            return {DEBUG_ERROR: "Other failure."}
    else:
        return {DEBUG_ERROR: "Use post"}


@app.route("/add_log_entry/", methods=['POST'])
@require_session_key
def add_log_entry():
    """Creates user in db

    Args:
    POST:
        id (str): User name
        pw (str): password

    Returns:
        json: failure message or id
    """
    if request.method == 'POST':
        loc_id = request.form.get('loc_id')
        if not db_get_location(int(loc_id)):
            return {DEBUG_ERROR: "Location ID does not exist."}
        pw = request.form.get('pw')
        new_user = {'id': id,
                    'password': pw}
        existing = db_get_user(new_user["id"])
        if existing:
            return {DEBUG_ERROR: "User exists."}
        try:
            db_add_user(new_user)
            return {DEBUG_MESSAGE: "User added"}
        except IntegrityError:
            return {DEBUG_ERROR: "Other failure."}
    else:
        return {DEBUG_ERROR: "Use post"}


@app.route("/init_db/")
@require_session_key
def init_db():
    """Make sure the db has been initialized...

    Args:
    GET:
        None

    Returns:
        json: Vague message
    """
    db.create_all()
    return {DEBUG_MESSAGE: "create_all called"}


if __name__ == '__main__':
    db.create_all()
    app.run()
