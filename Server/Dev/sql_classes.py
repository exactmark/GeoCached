
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, DECIMAL
from sqlalchemy.ext.declarative import declarative_base,DeclarativeMeta
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(String(250), primary_key=True)
    password = Column(String(250), nullable=False)
    # some_new_field = Column(String(250),nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserSession(Base):
    __tablename__ = 'usersession'

    id = Column(String(250), ForeignKey('user.id'), primary_key=True)
    session_key = Column(String(250), nullable=False)
    valid_through = Column(DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    obscured_url = Column(String(250))
    clear_url = Column(String(250))
    x_coord = Column(String(20))
    y_coord = Column(String(20))
    description = Column(String(250), nullable=True)
    log_entries = relationship("LogEntry")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class LogEntry(Base):
    __tablename__ = "logentry"

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer,ForeignKey('location.id'),nullable=False)
    user_id = Column(String(250), ForeignKey('user.id'), nullable=False)
    timestamp = Column(DateTime)
    text = Column(String(250))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



