# The database defintion
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Creating Database todo.db
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()
# Base is an object of declarative_base
Base = declarative_base()
# Data Definition
class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default = '')
    deadline = Column(Date, default = datetime.today())
    def __repr__(self):
        return str(self.id)+". "+self.task