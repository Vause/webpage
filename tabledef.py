from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
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
        self.password = password
        self.teacherFlag = teacherFlag
 
# create tables
Base.metadata.create_all(engine)
