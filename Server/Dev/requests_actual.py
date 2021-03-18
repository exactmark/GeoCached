import requests
import json

base_url = 'http://127.0.0.1:5000/'
# base_url = 'https://exactmark.pythonanywhere.com/'

user_list = [{'id': 'Mark', 'pw': 'WeakPw'},
             {'id': 'Vishal', 'pw': 'WeakPw'},
             {'id': 'Lakshmi', 'pw': 'WeakPw'}]

location_list = [
    {"name": "Mark's Place", "x_coord": "33.8704123", "y_coord": "-84.4675776", "description": "don't come here"},
    {"name": "Kroger", "x_coord": "33.8718565", "y_coord": "-84.4570496", "description": "A place for food."},
    {"name": "A Concrete Canoe", "x_coord": "33.9360701", "y_coord": "-84.5205357",
     "description": "This thing doesn't float"},
    {"name": "The Student Center", "x_coord": "33.9360701", "y_coord": "-84.5205357",
     "description": "I've studied here."}
]

image_list = {"Mark's Place": "seed_images/Mark.jpg",
              "Kroger": "seed_images/Kroger.jpg",
              "A Concrete Canoe": "seed_images/Canoe.jpg",
              "The Student Center": "seed_images/StudentCenter.jpg"}


def add_user(single_user):
    target_url = base_url + "add_single_user/"
    x = requests.post(target_url, data=single_user)
    print(x.text)


def add_location(single_location):
    target_url = base_url + "add_location/"
    x = requests.post(target_url, data=single_location)
    r_dict = json.loads(x.text)
    if "id" not in r_dict.keys():
        print(r_dict["debug_error"])
    else:
        files = {'file': (
            image_list[single_location["name"]].split("/")[-1], open(image_list[single_location["name"]], 'rb'),
            {'Expires': '0'})}
        data = {'loc_name': single_location["name"]}
        x = requests.post(base_url + 'put_location_image', files=files, data=data)
        print(x.text)


def seed_database():
    x = requests.get(base_url + "init_db/")
    for single_user in user_list:
        add_user(single_user)
    for single_location in location_list:
        add_location(single_location)


seed_database()

