from unittest import TestCase
from multiprocessing import Process
import requests
from sql_link import *

test_url_root = 'http://127.0.0.1:5000/'


def start_test_server():
    from geocached import app
    app.run()

class TestSql_link(TestCase):

    def get_root(self):
        url = test_url_root
        response = requests.get(url)
        self.assertEqual(response.text, "Caching with style")




    def ensure_server_active(self):
        try:
            self.get_root()
        except:
            import subprocess as sp
            process = sp.Popen('other_file.py', shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            out, err = process.communicate()  # The output and error streams.

    def test_get_location(self):
        self.ensure_server_active()
        url = test_url_root+'add_single_user/?id=Orange&pw=Bogus'
        response = requests.get(url)
        self.assertEqual(response.text,"failed to add")

