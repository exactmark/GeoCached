import time
from unittest import TestCase
from multiprocessing import Process
import requests
from sql_link import *

test_url_root = 'http://127.0.0.1:5000/'


def start_test_server():
    from geocached import app
    app.run()


class TestServerRoutes_link(TestCase):

    @classmethod
    def setUpClass(cls):
        import multiprocessing as mp
        mp.set_start_method('spawn')
        cls.server_process = mp.Process(target=start_test_server, args=())
        cls.server_process.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.server_process.terminate()
        print("done")

    def get_root(self):
        url = test_url_root
        response = requests.get(url)
        self.assertEqual(response.text, "Caching with style")

    def test_add_user_non_unique(self):
        url = test_url_root + 'add_single_user/?id=Orange&pw=Bogus'
        response = requests.get(url)
        self.assertEqual(response.text, "failed to add")

    def test_get_user(self):
        url = test_url_root + 'get_single_user/?id=Orange'
        response = requests.get(url)
        self.assertEqual(response.text, '{"id":"Orange","password":"Bogus"}\n')

    def test_add_location(self):
        url = test_url_root + "/add_location/?id=42&name=This%20is%20another%20location&x_coord=34.45&y_coord=-66,44"
        response = requests.get(url)
        url = test_url_root + "/add_location/?id=43&name=This%20is%20more%20location&x_coord=34.45&y_coord=-66,44"
        response = requests.get(url)


    def test_list_locations(self):
        url = test_url_root + "/get_location_list/"
        response = requests.get(url)
        self.assertGreaterEqual(len(response.text.split(",")),1)
