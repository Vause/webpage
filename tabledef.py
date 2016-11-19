from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash 
engine = create_engine('mysql+pymysql://test_1:testthisisatest1234@104.131.96.183/TeamYellow', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
    """"""
    __tablename__ = "TestLogin"
 
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    teacherFlag = Column(Boolean, default = True)
 
    #----------------------------------------------------------------------
    def __init__(self, username, password, teacherFlag):
        """"""
        self.username = username
        self.set_password(password)
        self.teacherFlag = teacherFlag

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
 
# create tables
Base.metadata.create_all(engine)
