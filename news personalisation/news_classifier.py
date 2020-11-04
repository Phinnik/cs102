from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bayes import NaiveBayesClassifier


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
Session = sessionmaker(bind=engine)
s = Session()

news = s.query(News).all()

titles = [n.title for n in news]
labels = [n.label for n in news]

X = titles[:800]
y = labels[:800]

X_test = titles[800:900]
y_test = titles[800:900]


max_score = -1
best_alpha = -1
for i in range(1, 100):
	alpha = i/100
	nbc = NaiveBayesClassifier(1)
	nbc.fit(X, y)
	score = nbc.score(X_test, y_test)
	if score > max_score:
		max_score = score
		best_alpha = alpha
#try to know best alpha
print('alpha: {}, score: {}'.format(best_alpha, max_score))



from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

model = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB(alpha=0.05)),
])

model.fit(X, y)
sklearn_score = model.score(X_test, y_test)

# sklearn also doesn't work :(
print(sklearn_score)