
from sql_classes import User, UserSession, Location, LogEntry

def get_location(location_id):
    # This will run a query on the db for the location with id location_id
    found_location =Location(id=-1,name="The first place",x_coord=12,y_coord=13,description="A place description")
    return found_location.as_dict()


