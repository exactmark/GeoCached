from unittest import TestCase
from multiprocessing import Process
import requests
from sql_link import *
import json

db_loc = 'sqlite:///:memory:'


# 'sqlite:///test.db'

test_users = [{"id":"TestUser1","password":"TestPassword1"},
              {"id":"TestUser2","password":"TestPassword2"},]

class TestSql_link(TestCase):

    @classmethod
    def setUpClass(self):
        self.sql_link = sql_link(db_loc)
        for single_user in test_users:
            # single_json = json.dumps(single_user,indent=4)
            # print(single_json)
            self.sql_link.add_user(single_user)

    @classmethod
    def tearDownClass(self):
        print("done")

    def test_add_user(self):
        pass

    def test_get_user(self):
        TestUser1 = self.sql_link.get_user("TestUser1")
        self.assertEqual(TestUser1["password"],"TestPassword1")

    def test_add_location(self):
        pass

    def test_get_location(self):
        pass
