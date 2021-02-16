from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sql_classes import Base
from sql_classes import *
import json


class sql_link(object):
    Session = None
    engine = None

    def __init__(self, db_location=None):
        self.init_db(db_location)

    def init_db(self, db_location='sqlite:///:memory:'):
        self.engine = create_engine(db_location, echo=True)
        Base.metadata.create_all(self.engine)

    def create_db_link(self):
        if self.engine is None:
            self.init_db()
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    def get_location(self, location_id: int):
        # Returns a location given a single ID
        found_location = Location(id=-1, name="The first place", x_coord=12, y_coord=13,
                                  description="A place description")
        return found_location.as_dict()

    def add_location(self, location_json: json):
        new_location = Location()
        new_location = set_columns_from_json(new_location, location_json)

    def get_user(self, user_id: str):
        session = self.Session()
        result = session.query(User).filter_by(id=user_id).first()
        if result:
            return result.as_dict()
        else:
            return {}

    def add_user(self, json_data: json):
        new_obj = User()
        new_obj = set_columns_from_json(new_obj, json_data)
        session = self.Session()
        session.add(new_obj)
        session.commit()


def set_columns_from_json(new_object: object, input_json: json):
    attribute_list = [attrname for attrname in dir(new_object) if attrname[:1] != "_"]
    print(attribute_list)
    for single_key in input_json.keys():
        if single_key in attribute_list:
            setattr(new_object, single_key, input_json[single_key])
    return new_object
