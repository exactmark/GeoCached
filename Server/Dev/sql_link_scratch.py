import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from sql_classes import Base, User, UserSession

# Create an engine that stores data in the local directory's


# sqlalchemy_example.db file.
# engine = create_engine('sqlite:///sqlalchemy_example.db')
engine = create_engine('sqlite:///:memory:', echo=True)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
one_user = User(id="Red", password="RedPW")
session.add(one_user)
session.add_all([
    User(id='Green', password='GreenPW'),
    User(id='Blue', password='BluePW'),
    User(id='Yellow', password='YellowPW')])
# print(one_user.id)
# print(session.new)
session.commit()

red_session = UserSession(id="Bread", session_key="redsesskey")
print(red_session.id)
session.commit()

result = session.query(User).filter_by(id='Red').first()

print(result.id)
# print(result.password)
