from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker



Base = declarative_base()
engine = create_engine('sqlite:///users.db')
session = sessionmaker(bind=engine)

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	age = Column(Integer)
	fullname = Column(String)
	password = Column(String)

Base.metadata.create_all(engine)

users = [User(name='phil', age=18, fullname='Philipp Zdorov', password='123'),
		 User(name='leha', age=18, fullname='Alexey Samoshenkov', password='3256'),
		 User(name='liza', age=18, fullname='Elizaveta Mahotina', password='23546576'),
		 User(name='lesya', age=20, fullname='Olesya Borzenkova', password='23456'),
		 User(name='nataga', age=19, fullname='Natalya Krivonos', password='324')]

s = session()
s.add_all(users)
s.commit()