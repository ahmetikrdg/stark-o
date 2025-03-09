import joblib


def modelLoad():
    global vectorizer, model
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    model = joblib.load('sgd_model.pkl')
