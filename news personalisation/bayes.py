from typing import List
from collections import defaultdict, Counter
import string
from math import log


class NaiveBayesClassifier:
    
    def __init__(self, alpha: float):
        self.alpha = alpha

    def text_format(self, text: str) -> str:
        # lowering case and replacing symbols
        text = text.lower()
        translator = str.maketrans("", "", string.punctuation)
        return text.translate(translator)

    def fit(self, X: List, y: List) -> None:
        """ Fit Naive Bayes classifier according to X, y. """

        labels = set(y)
        self.labels = set(y)
        labels.update({'amount'})

        words_dict = defaultdict(lambda: {l: 0 for l in labels})
        amount_counter = Counter()

        self.class_probabilities = {l: 0 for l in self.labels}
        for l in self.labels:
            self.class_probabilities[l] = y.count(l) / len(y)

        for i, doc in enumerate(X):
            
            doc = self.text_format(doc)
            doc_words = doc.split(' ')

            for word in doc_words:
                #if len(word) <= 2:
                #    continue
                #if word[-1] == 's':
                #    word = word[:-1]
                #
                words_dict[word][y[i]] += 1
                words_dict[word]['amount'] += 1
                amount_counter[y[i]] += 1

        self.vector_amount = len(words_dict.items())
        word_probabilities =  defaultdict(lambda: {l: 0 for l in self.labels})

        for word in words_dict:
            for label in self.labels:
                word_probabilities[word][label] = (words_dict[word][label] + self.alpha)/(amount_counter[label] + self.alpha*self.vector_amount)

        self.word_probabilities = word_probabilities


    def predict(self, doc: str) -> str:
        """ Perform classification on an array of test vector X """
        doc = self.text_format(doc)
        doc_words = doc.split(' ')

        doc_probabilities = {l: log(self.class_probabilities[l]) for l in self.labels}
        for l in self.labels:
            for word in doc_words:
                if word in self.word_probabilities:
                    doc_probabilities[l] += log(self.word_probabilities[word][l])

                else:
                    unknown_probability = 0
                    doc_probabilities[l] += 0

        prediction = max(doc_probabilities, key=doc_probabilities.get)
        return prediction

        
    
    def score(self, X_test: List, y_test: List) -> float:
        """ Returns the mean accuracy on the given test data and labels. """
        right = 0
        for i, doc in enumerate(X_test):
            if self.predict(doc) == y_test[i]:
                right += 1

        return right / len(X_test)

        