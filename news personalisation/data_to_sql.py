from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data import data


Base = declarative_base()

class News(Base):
	__tablename__ = "news personalisation"
	id = Column(Integer, primary_key = True)
	title = Column(String)
	author = Column(String)
	url = Column(String)
	comments = Column(Integer)
	points = Column(Integer)
	label = Column(String)

engine = create_engine("sqlite:///news personalisation.db")
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)


def data_to_sql() -> None:
	# Puts data to DB
	for i, news in enumerate(data):
		data[i] = News(title = news['title'],
					   author = news['author'],
					   url = news['url'],
					   comments = news['comments'],
					   points = news['points'],
					   label = news['label'])

	s = session()
	s.add_all(data)
	s.commit()
