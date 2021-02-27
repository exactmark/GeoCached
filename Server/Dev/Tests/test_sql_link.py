from unittest import TestCase
from multiprocessing import Process
import requests
from sql_link import *
import json

db_loc = 'sqlite:///:memory:'


# 'sqlite:///test.db'

base_users = [{"id": "TestUser1", "password": "TestPassword1"},
              {"id": "TestUser2", "password": "TestPassword2"}]
base_locations = [{"id": "0", "name": "Test Location 0", "x_coord": "1", "y_coord": "1",
                   "description": "Quadrant 1"},
                  {"id": "1", "name": "Test Location 1", "x_coord": "-1", "y_coord": "1",
                   "description": "Quadrant 2"},
                  {"id": "2", "name": "Test Location 2", "x_coord": "-1", "y_coord": "-1",
                   "description": "Quadrant 3"},
                  {"id": "3", "name": "Test Location 3", "x_coord": "1", "y_coord": "-1",
                   "description": "Quadrant 4"}
                  ]


class TestSql_link(TestCase):

    @classmethod
    def setUpClass(self):
        self.sql_link = sql_link(db_loc)
        self.add_base_users()
        self.add_base_locations()

    @classmethod
    def add_base_users(self):

        for single_user in base_users:
            # single_json = json.dumps(single_user,indent=4)
            # print(single_json)
            self.sql_link.add_user(single_user)

    @classmethod
    def add_base_locations(self):
        for single_location in base_locations:
            self.sql_link.add_location(single_location)

    @classmethod
    def tearDownClass(self):
        print("done")

    def test_add_new_user(self):
        new_user = {"id": "TestAdd", "password": "TestPassword1"}
        self.sql_link.add_user(new_user)
        UserFind = self.sql_link.get_user(new_user["id"])
        self.assertEqual(new_user["password"], UserFind["password"])

    def test_get_user(self):
        TestUser1 = self.sql_link.get_user("TestUser1")
        self.assertEqual(TestUser1["password"], "TestPassword1")

    def test_add_location(self):
        testing_location = {"id": "4", "name": "Test From Add", "x_coord": "1", "y_coord": "1",
                           "description": "Quadrant 1"}
        self.sql_link.add_location(testing_location)
        just_added = self.sql_link.get_location(4)
        self.assertEqual(testing_location["name"],just_added["name"])

    def test_list_location_ids(self):
        retrieved_ids = self.sql_link.list_location_ids()
        base_location_ids = [int(single_location["id"]) for single_location in base_locations]

        self.assertEqual(len(set(base_location_ids).intersection(set(retrieved_ids))),
                         len(base_locations))

    def test_get_location(self):
        result = self.sql_link.get_location(0)
        self.assertEqual(result["description"],"Quadrant 1")