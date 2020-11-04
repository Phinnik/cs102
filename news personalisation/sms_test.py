import csv
from pprint import pprint as pp
from bayes import NaiveBayesClassifier


with open('spam.csv', newline='') as f:
	reader = csv.reader(f, delimiter=',')
	data = list(reader)[1:]


docs = [d[1] for d in data]
labels = [d[0] for d in data]



nbc = NaiveBayesClassifier(0.6)
X_train, y_train = docs[:4500], labels[:4500]
X_test, y_test = docs[4500:], labels[4500:]
nbc.fit(X_train, y_train)
my_score = nbc.score(X_test, y_test)





from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

model = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB(alpha=0.05)),
])

model.fit(X_train, y_train)
sklearn_score = model.score(X_test, y_test)

print('my: {}; sklearn: {}'.format(my_score, sklearn_score))