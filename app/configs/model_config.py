import os

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier

if not os.path.exists('tfidf_vectorizer.pkl'):
    print("'tfidf_vectorizer.pkl' not found, creating a new TfidfVectorizer.")
    vectorizer = TfidfVectorizer()
    joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
else:
    vectorizer = joblib.load('tfidf_vectorizer.pkl')

if not os.path.exists('sgd_model.pkl'):
    print("'sgd_model.pkl' not found, creating a new SGDClassifier.")
    model = SGDClassifier()
    joblib.dump(model, 'sgd_model.pkl')
else:
    model = joblib.load('sgd_model.pkl')

excel_path = "data.xlsx"
