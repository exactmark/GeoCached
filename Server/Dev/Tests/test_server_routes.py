import time
from unittest import TestCase
from multiprocessing import Process
import requests
import globals
from geocached import DEBUG_ERROR, DEBUG_MESSAGE
import json

test_url_root = 'http://127.0.0.1:5000/'

user_list = [{'id': 'Red', 'pw': 'RedPW'},
             {'id': 'Orange', 'pw': 'OrangePW'},
             {'id': 'Mark', 'pw': 'WeakPw'},
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


def start_test_server():
    from geocached import app, db
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///:memory:'
    db.create_all()
    globals.debug_mode = True
    app.run()


class TestServerRoutes_link(TestCase):

    @classmethod
    def setUpClass(cls):
        import multiprocessing as mp
        mp.set_start_method('spawn')
        cls.server_process = mp.Process(target=start_test_server, args=())
        cls.server_process.start()
        # this sleep does not appear to be necessary
        # time.sleep(1)

    def add_user(self, user_info):
        url = test_url_root + 'add_single_user/'
        response = requests.post(url, data=user_info)
        return response

    @classmethod
    def tearDownClass(cls):
        cls.server_process.terminate()
        # print("done")

    def get_root(self):
        url = test_url_root
        response = requests.get(url)
        self.assertEqual(response.text, "Caching with style")

    def test_add_user_non_unique(self):
        self.add_user(user_list[0])
        response = self.add_user(user_list[0])
        self.assertEqual(self.get_dict_from_url_response(response)[DEBUG_ERROR], "User exists.")

    def test_get_user(self):
        self.add_user(user_list[1])
        url = test_url_root + 'get_single_user/?id=Orange'
        response = requests.get(url)
        self.assertEqual(response.text, '{"id":"Orange","password":"","score":0}\n')

    def test_add_location(self):
        url = test_url_root + "add_location/"

        for single_location in location_list:
            self.add_session_key(single_location)
            x = requests.post(url, single_location)
            response = requests.get(url)

        url = test_url_root + "get_location_list/"
        response = requests.get(url)
        loc_ids = set(response.text.split(","))
        small_list = loc_ids.intersection({"1", "2"})
        self.assertEqual(2, len(small_list))

    def add_session_key(self, new_data):
        self.add_user(user_list[0])
        target_url = test_url_root + "login"
        a_user = user_list[0]
        x = requests.post(target_url, a_user)
        new_data["session_key"] = json.loads(x.text)["session_key"]
        return new_data

    def test_list_locations(self):
        url = test_url_root + "get_location_list/"
        response = requests.get(url)
        self.assertGreaterEqual(len(response.text.split(",")), 1)

    def test_login_failure_bad_user(self):
        single_user = user_list[0]
        single_user['id'] = "BogusUser2"
        url = test_url_root + "login/"
        response = requests.post(url, data=single_user)
        # print("bad_user_response %s"%response.text)
        response_dict = self.get_dict_from_url_response(response)
        self.assertEqual(response_dict[DEBUG_ERROR], 'No user entry.')

    def test_login_failure_bad_password(self):
        single_user = user_list[0]
        single_user['pw'] = "BogusPW"
        url = test_url_root + "login/"
        response = requests.post(url, data=single_user)
        response_dict = self.get_dict_from_url_response(response)
        # print(response_dict)
        self.assertEqual(response_dict[DEBUG_ERROR], 'Bad password.')

    def test_login_successful_login(self):
        self.add_user(user_list[0])
        url = test_url_root + "login/"
        response = requests.post(url, data=user_list[0])
        response_dict = self.get_dict_from_url_response(response)
        if DEBUG_ERROR in response_dict.keys():
            self.assertEqual(True, False, "Successful login provoked error")
        if "session_key" not in response_dict.keys():
            self.assertEqual(True, False, "Session key not returned")
        session_key = response_dict["session_key"]
        self.assertEqual(len(session_key), 36)
        self.assertEqual(len(session_key.split("-")), 5)

    def test_score_functions(self):
        self.add_user(user_list[1])
        url = test_url_root + 'get_user_score/?id=Orange'
        response = requests.get(url)
        self.assertEqual(json.loads(response.text)['score'], 0)
        url = test_url_root + 'put_user_score'
        data = {'id': "Orange", 'score': 10}
        data = self.add_session_key(data)
        response = requests.post(url, data)
        url = test_url_root + 'get_user_score/?id=Orange'
        response = requests.get(url)
        self.assertEqual(json.loads(response.text)['score'], 10)

    def get_dict_from_url_response(self, url_response) -> dict:
        response_text = url_response.text.lstrip()
        return json.loads(response_text)
