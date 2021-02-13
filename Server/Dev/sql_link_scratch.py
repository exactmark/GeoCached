import os
import sys
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from sql_classes import Base, User, UserSession

from sql_link import sql_link

my_link = sql_link('sqlite:///test.db')

my_link.create_db_link()
# input("yo")
session = my_link.Session()
# one_user = User(id="Red", password="RedPW")
# session.add(one_user)
# session.add_all([
#
#     User(id='Green', password='GreenPW'),
#     User(id='Blue', password='BluePW'),
#     User(id='Yellow', password='YellowPW')])
# # print(one_user.id)
# # print(session.new)
# session.commit()
#
# red_session = UserSession(id="Bread", session_key="redsesskey")
# print(red_session.id)
# session.commit()

result = session.query(User).filter_by(id='Red').first()

print(result.id)
# print(result.password)
