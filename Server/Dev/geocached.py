import math

from sqlalchemy.exc import IntegrityError
import json
import os
from flask import Flask, flash, request, redirect, url_for, jsonify
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
REQUIRE_SESSION_KEY = True
SAME_LOCATION_THRESHOLD_IN_KILOMETERS = 0.05

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
    score = db.Column(db.Integer)

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
    log_entries = db.relationship("LogEntry",cascade="all, delete-orphan")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class LogEntry(Base):
    __tablename__ = "logentry"

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    user_id = db.Column(db.String(250), db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
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
    # print(result)
    db.session.close()
    if result:
        return result.as_dict()
    else:
        return None


def db_test_for_location_add_error(new_location):
    if db_get_location_by_name(new_location["name"]):
        return {DEBUG_ERROR: "Location is duplicate"}
    other_location = db_location_too_close(new_location)
    if other_location:
        return {DEBUG_ERROR: "Location is too close, id:" + str(other_location.id)}
    else:
        return None


def db_location_too_close(new_location):
    all_locations = db.session.query(Location)
    for single_location in all_locations:
        distance = get_location_distance(single_location, new_location)
        if distance < SAME_LOCATION_THRESHOLD_IN_KILOMETERS:
            return single_location
    return None


def get_location_distance(single_location, new_location):
    # this part needs to be further tested
    earthRadiusKm = 6371
    lon1 = float(single_location.y_coord)
    lat1 = float(single_location.x_coord)
    lon2 = float(new_location["y_coord"])
    lat2 = float(new_location["x_coord"])
    distance_in_km = distanceInKmBetweenEarthCoordinates(lat1, lon1, lat2, lon2)
    return distance_in_km


def degreesToRadians(degrees):
    return degrees * math.pi / 180.00


def distanceInKmBetweenEarthCoordinates(lat1, lon1, lat2, lon2):
    # as shamelessly pulled from https://stackoverflow.com/questions/365826/calculate-distance-between-2-gps-coordinates
    earthRadiusKm = 6371

    dLat = degreesToRadians(lat2 - lat1)
    dLon = degreesToRadians(lon2 - lon1)

    lat1 = degreesToRadians(lat1)
    lat2 = degreesToRadians(lat2)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(
        lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earthRadiusKm * c


def db_add_location(location_json: json):
    new_location = Location()
    new_location = set_columns_from_json(new_location, location_json)
    db.session.add(new_location)
    db.session.commit()
    loc_id = new_location.id
    db.session.close()
    return loc_id

def db_delete_location(location_id:int):
    result = db.session.query(Location).filter_by(id=location_id).first()
    if result:
        db.session.delete(result)
        db.session.commit()
        db.session.close()
        return "success"
    return "no location"



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


def db_update_user_score(user_id, score):
    result = db.session.query(User).filter_by(id=user_id).first()
    result.score = score
    db.session.commit()
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


def db_add_log_entry(json_data: json):
    new_obj = LogEntry()
    new_obj = set_columns_from_json(new_obj, json_data)
    db.session.add(new_obj)
    db.session.commit()
    log_id = new_obj.id
    db.session.close()
    return log_id

def db_delete_log_entry(log_id:int):
    result = db.session.query(LogEntry).filter_by(id=log_id).first()
    if result:
        db.session.delete(result)
        db.session.commit()
        db.session.close()
        return "success"
    return "no log entry"


def db_get_logs(location_id: int):
    result = db.session.query(LogEntry).filter_by(location_id=location_id).all()
    db.session.close()

    if result:
        # return_result = []
        # for row in result:
        #
        #     return_result.append( row.as_dict())
        # return return_result
        return_result = []
        return_dict = {}
        for row in result:
            return_result.append(row.as_dict())
        for x in range(0, len(return_result)):
            return_dict[x] = return_result[x]
        return return_dict
    else:
        return None

def db_get_most_recent_log_entry():
    result = db.session.query(LogEntry).order_by(LogEntry.timestamp.desc()).first()
    db.session.close()
    return result.as_dict()


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
        # print(db_get_session_owner(session_key))
        return func(*args, **kwargs)

    return wrapper


# **************
# ROUTES START
# **************


@app.route('/')
def hello_world():
    return 'Caching with style'


@app.route("/get_location_list/")
# @require_session_key
def get_location_list():
    """Gets a list of locations currently in the db.

    Args:

    Returns:
        string: a comma separated list of id numbers
    """
    return db_list_location_ids()


@app.route("/get_single_location/")
# @require_session_key
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
# @require_session_key
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
# @require_session_key
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
    # not multi process safe
    new_location = {"name": request.form.get("name"),
                    "x_coord": request.form.get("x_coord"),
                    "y_coord": request.form.get("y_coord"),
                    "description": request.form.get("description")}

    try:
        location_error = db_test_for_location_add_error(new_location)
        if location_error:
            return location_error
        loc_id = db_add_location(new_location)
        return {DEBUG_MESSAGE: "success", "id": loc_id}
    except IntegrityError:
        return {DEBUG_ERROR: "failed to add"}


@app.route("/delete_location/", methods=['POST'])
# @require_session_key
def delete_location():
    """Allows deletion of a location

    Args:
    POST:
        name (str): The location name. Currently being checked for uniqueness
        x_coord (str): Latitude
        y_coord (str): Longitude
        description (str): A short description

    Returns:
        json: success/failure
    """
    loc_id = request.form.get("id")

    message = db_delete_location(loc_id)
    return {DEBUG_MESSAGE: message, "id": loc_id}



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
        return {DEBUG_ERROR: "No user entry."}
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
# @require_session_key
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
# @require_session_key
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
        score = request.form.get('score')
        if not score:
            score = 0
        new_user = {'id': id,
                    'password': pw,
                    'score': score}
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
# @require_session_key
def add_log_entry():
    """Creates user in db

    Args:
    POST:
        loc_id (int): Location id from locations table
        user_id (str): User name
        text (str): The text of the message

    Returns:
        json: failure message or id
    """
    if request.method == 'POST':
        loc_id = request.form.get('loc_id')
        if loc_id is None:
            return {DEBUG_ERROR: "Location ID not provided."}
        if not db_get_location(int(loc_id)):
            return {DEBUG_ERROR: "Location ID does not exist."}
        new_log_entry = {'location_id': request.form.get('loc_id'),
                         'user_id': request.form.get('user_id'),
                         'text': request.form.get('text')}
        new_log_id = db_add_log_entry(new_log_entry)
        return {DEBUG_MESSAGE: "newLogID = %d" % new_log_id}
    else:
        return {DEBUG_ERROR: "Use post"}

@app.route("/delete_log_entry/", methods=['POST'])
# @require_session_key
def delete_log_entry():
    """deletes log entry

    Args:
    POST:
        log_id (int): log id from logentry table

    Returns:
        json: failure message or id
    """
    log_id = request.form.get("id")

    message =db_delete_log_entry(log_id)
    return {DEBUG_MESSAGE: message, "id": log_id}



@app.route("/get_log_entries/")
# @require_session_key
def get_log_entries():
    """Gets json for single location

    Args:
    GET:
        loc_id (int): The index to retrieve

    Returns:
        json: location information
    """
    location_id = request.args.get('loc_id')
    if location_id:
        location = db_get_location(location_id)
        if not location:
            return {DEBUG_ERROR: "location not found"}
        else:
            logs = db_get_logs(location_id)
            if logs:
                return logs
            else:
                return {DEBUG_MESSAGE: "No logs for this location"}
    else:
        return {DEBUG_ERROR: "no location id"}


@app.route("/get_most_recent_log/")
# @require_session_key
def get__most_recent_log():
    """Gets id and time of most recent log entry

    Args:
    GET:
        no args

    Returns:
        json: location information
    """
    result = db_get_most_recent_log_entry()
    return result


@app.route("/get_user_score/")
# @require_session_key
def get_user_score():
    """Gets user score

    Args:
    GET:
        user_id (str): The index to retrieve

    Returns:
        json: score information
    """
    user_id = request.args.get('id')
    user = db_get_user(user_id)
    if user:
        user["password"] = ""
        return user
    else:
        return {DEBUG_ERROR: "No user found."}


@app.route("/put_user_score/", methods=['POST'])
# @require_session_key
def put_user_score():
    """Sets user score

    Args:
    POST:
        id (str): The user to set
        score (int): the new score
    Returns:
        json: new score if successful, else error message
    """
    user_id = request.form.get('id')
    score = request.form.get('score')
    user = db_get_user(user_id)
    if user and score:
        db_update_user_score(user_id, score)
        return user
    else:
        return {DEBUG_ERROR: "No user found."}


@app.route("/init_db/")
# @require_session_key
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
