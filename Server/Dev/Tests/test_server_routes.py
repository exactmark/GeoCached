import time
from unittest import TestCase
from multiprocessing import Process
import requests
import globals
from geocached import DEBUG_ERROR
import json

test_url_root = 'http://127.0.0.1:5000/'


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
        url = test_url_root + 'add_single_user/?id=Red&pw=RedPW'
        response = requests.get(url)
        url = test_url_root + 'add_single_user/?id=Orange&pw=OrangePw'
        response = requests.get(url)

    @classmethod
    def tearDownClass(cls):
        cls.server_process.terminate()
        # print("done")

    def get_root(self):
        url = test_url_root
        response = requests.get(url)
        self.assertEqual(response.text, "Caching with style")

    def test_add_user_non_unique(self):
        url = test_url_root + 'add_single_user/?id=Orange&pw=OrangePw'
        response = requests.get(url)
        self.assertEqual(self.get_dict_from_url_response(response)[DEBUG_ERROR], "User exists.")

    def test_get_user(self):
        url = test_url_root + 'get_single_user/?id=Orange'
        response = requests.get(url)
        self.assertEqual(response.text, '{"id":"Orange","password":"OrangePw"}\n')

    def test_add_location(self):
        url = test_url_root + "add_location/?id=42&name=This%20is%20another%20location&x_coord=34.45&y_coord=-66,44"
        response = requests.get(url)
        url = test_url_root + "add_location/?id=43&name=This%20is%20more%20location&x_coord=34.45&y_coord=-66,44"
        response = requests.get(url)
        url = test_url_root + "get_location_list/"
        response = requests.get(url)
        loc_ids = set(response.text.split(","))
        small_list = loc_ids.intersection({"42", "43"})
        self.assertEqual(len(small_list), 2)

    def test_list_locations(self):
        url = test_url_root + "get_location_list/"
        response = requests.get(url)
        self.assertGreaterEqual(len(response.text.split(",")), 1)

    def test_login_failure_bad_user(self):
        url = test_url_root + "login/"
        response = requests.get(url)
        response_dict = self.get_dict_from_url_response(response)
        self.assertEqual(response_dict[DEBUG_ERROR], 'No user entry.')

    def test_login_failure_bad_password(self):
        url = test_url_root + "login/?id=Red&pw=BogusPw"
        response = requests.get(url)
        response_dict = self.get_dict_from_url_response(response)
        self.assertEqual(response_dict[DEBUG_ERROR], 'Bad password.')

    def test_login_successful_login(self):
        url = test_url_root + "login/?id=Red&pw=RedPW"
        response = requests.get(url)
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
