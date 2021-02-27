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
        self.create_db_link()

    def init_db(self, db_location='sqlite:///:memory:'):
        self.engine = create_engine(db_location, echo=True)
        Base.metadata.create_all(self.engine)

    def create_db_link(self):
        if self.engine is None:
            self.init_db()
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    def get_location(self, location_id: int):
        print("Location id is %d"%location_id)
        result = self.Session().query(Location).filter_by(id=location_id).first()
        # print(result)
        if result:
            return result.as_dict()
        else:
            return {}

    def add_location(self, location_json: json):
        new_location = Location()
        new_location = set_columns_from_json(new_location, location_json)
        session = self.Session()
        session.add(new_location)
        session.commit()

    def list_location_ids(self):
        session = self.Session()
        result = [instance.id for instance in session.query(Location.id)]
        return result

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
    # print(attribute_list)
    for single_key in input_json.keys():
        if single_key in attribute_list:
            setattr(new_object, single_key, input_json[single_key])
    return new_object
