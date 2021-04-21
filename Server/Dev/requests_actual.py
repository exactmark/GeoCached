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
    {"name": "The Student Center", "x_coord": "33.9410821", "y_coord": "-84.5206215",
     "description": "I've studied here."}
]

image_list = {"Mark's Place": "seed_images/Mark.jpg",
              "Kroger": "seed_images/Kroger.jpg",
              "A Concrete Canoe": "seed_images/Canoe.jpg",
              "The Student Center": "seed_images/StudentCenter.jpg"}

log_entry_list = [{'loc_id': 1,
                   'user_id': 'Mark',
                   'text': 'This is a note about Marks place'},
                  {'loc_id': 1,
                   'user_id': 'Mark',
                   'text': 'This is a second note about Marks place'},
                  {'loc_id': 2,
                   'user_id': 'Mark',
                   'text': 'I love going to KROGER'},
                  {'loc_id': 2,
                   'user_id': 'Stella',
                   'text': 'I do not check if the user is legit!'},
                  {'loc_id': 3,
                   'user_id': 'Mark',
                   'text': 'Up the crick'},
                  {'loc_id': 3,
                   'user_id': 'Mark',
                   'text': 'With an iron paddle'},
                  {'loc_id': 4,
                   'user_id': 'Mark',
                   'text': 'Do not remind me'},
                  {'loc_id': 4,
                   'user_id': 'Mark',
                   'text': 'I should really have better text here'}
                  ]


def add_user(single_user):
    target_url = base_url + "add_single_user/"
    x = requests.post(target_url, data=single_user)
    print(x.text)


def add_location(single_location):
    target_url = base_url + "add_location/"
    single_location = add_session_key(single_location)
    x = requests.post(target_url, data=single_location)
    r_dict = json.loads(x.text)
    if "id" not in r_dict.keys():
        print(x.text)
    else:
        files = {'file': (
            image_list[single_location["name"]].split("/")[-1], open(image_list[single_location["name"]], 'rb'),
            {'Expires': '0'})}
        data = {'loc_name': single_location["name"]}
        data = add_session_key(data)
        x = requests.post(base_url + 'put_location_image', files=files, data=data)
        print(x.text)


def add_log_entry(single_log):
    target_url = base_url + "add_log_entry/"
    single_log = add_session_key(single_log)
    x = requests.post(target_url, data=single_log)
    print(x.text)


def add_session_key(new_data):
    target_url = base_url + "login"
    a_user = user_list[0]
    x = requests.post(target_url, a_user)
    new_data["session_key"] = json.loads(x.text)["session_key"]
    return new_data


def test_user_score():
    print("no")


def seed_database():
    x = requests.get(base_url + "init_db/")
    for single_user in user_list:
        add_user(single_user)
    for single_location in location_list:
        add_location(single_location)
    for single_log in log_entry_list:
        add_log_entry(single_log)


seed_database()
