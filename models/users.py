# http://flask.pocoo.org/docs/0.11/patterns/sqlalchemy/
# http://colanderalchemy.readthedocs.io/en/latest/examples.html
from sqlalchemy import Column, Integer, String, Enum
from app import Base


class Users(Base):
    __tablename__ = 'users'
    uuid = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(320), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum('Male', 'Female', 'Other'), nullable=False)

    def __init__(self, name=None, email=None):
    	self.name = name
    	self.email = email

    def __repr__(self):
    	return self.uuid