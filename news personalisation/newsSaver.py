from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hackerNewsParser import get_news



Base = declarative_base()
engine = create_engine("sqlite:///news personalisation.db")
session = sessionmaker(bind=engine)

class News(Base):
	__tablename__ = "news personalisation"
	id = Column(Integer, primary_key = True)
	title = Column(String)
	author = Column(String)
	url = Column(String)
	comments = Column(Integer)
	points = Column(Integer)
	label = Column(String)

Base.metadata.create_all(bind=engine)

news_list = get_news(n_pages=34)
s = session()

for i in range(len(news_list)):
	news_list[i] = News(title = news_list[i]['title'],
						author = news_list[i]['author'],
						url = news_list[i]['url'],
						comments = news_list[i]['comments'],
						points = news_list[i]['points'],
						label = news_list[i]['label'])

s.add_all(news_list)
s.commit()