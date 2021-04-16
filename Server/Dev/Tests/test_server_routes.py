import time
from unittest import TestCase
from multiprocessing import Process
import requests
import globals
from geocached import DEBUG_ERROR
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
    {"name": "The Student Center", "x_coord": "33.9360701", "y_coord": "-84.5205357",
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

    def add_uesr(self, user_info):
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
        self.add_uesr(user_list[0])
        response = self.add_uesr(user_list[0])
        self.assertEqual(self.get_dict_from_url_response(response)[DEBUG_ERROR], "User exists.")

    def test_get_user(self):
        self.add_uesr(user_list[1])
        url = test_url_root + 'get_single_user/?id=Orange'
        response = requests.get(url)
        self.assertEqual(response.text, '{"id":"Orange","password":""}\n')

    def test_add_location(self):
        url = test_url_root + "add_location/"

        for single_location in location_list:
            x = requests.post(url, single_location)
            response = requests.get(url)

        url = test_url_root + "get_location_list/"
        response = requests.get(url)
        loc_ids = set(response.text.split(","))
        small_list = loc_ids.intersection({"0", "1"})
        self.assertEqual(2, len(small_list))

    def test_list_locations(self):
        url = test_url_root + "get_location_list/"
        response = requests.get(url)
        self.assertGreaterEqual(len(response.text.split(",")), 1)

    def test_login_failure_bad_user(self):
        single_user = user_list[0]
        single_user['id'] = "BogusUser"
        url = test_url_root + "login/"
        response = requests.post(url, data=single_user)
        response_dict = self.get_dict_from_url_response(response)
        self.assertEqual(response_dict[DEBUG_ERROR], 'No user entry.')

    def test_login_failure_bad_password(self):
        single_user = user_list[0]
        single_user['pw'] = "BogusPW"
        url = test_url_root + "login/"
        response = requests.post(url, data=single_user)
        response_dict = self.get_dict_from_url_response(response)
        print(response_dict)
        self.assertEqual(response_dict[DEBUG_ERROR], 'Bad password.')

    def test_login_successful_login(self):
        self.add_uesr(user_list[0])
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

    def get_dict_from_url_response(self, url_response) -> dict:
        response_text = url_response.text.lstrip()
        return json.loads(response_text)
