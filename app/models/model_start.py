import joblib
import pandas as pd
import seaborn as sns

from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, auc, roc_curve, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from app.utils import clean_text

from app.configs.model_config import excel_path
from app.utils.write_results_to_json import write_results_to_json


def modelStart():
    df_train = pd.read_excel(excel_path, sheet_name='Train Data')
    df_test = pd.read_excel(excel_path, sheet_name='Test Data')

    df_train['text'] = df_train['text'].astype(str)
    df_train['text'] = df_train['text'].apply(clean_text.clean_text)
    comments_train = df_train['text'].tolist()
    labels_train = df_train['labels'].tolist()

    df_test['text'] = df_test['text'].apply(clean_text.clean_text)
    comments_test = df_test['text'].tolist()
    labels_test = df_test['labels'].tolist()

    unique_labels = ['TARAFSIZ', 'OLUMLU', 'OLUMSUZ']
    label_encoder = LabelEncoder()
    label_encoder.fit(unique_labels)

    print(list(zip(label_encoder.classes_, range(len(label_encoder.classes_)))))

    vectorizer = TfidfVectorizer(ngram_range=(1, 3))
    X_train = vectorizer.fit_transform(comments_train)
    y_train = label_encoder.transform(labels_train)

    joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    model = SGDClassifier(loss='log_loss', penalty='l2', alpha=0.0001)
    model.fit(X_train_resampled, y_train_resampled)

    X_test = vectorizer.transform(comments_test)
    y_test = label_encoder.transform(labels_test)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')

    joblib.dump(model, 'sgd_model.pkl')

    y_probs = model.predict_proba(X_test)[:, 1]

    write_results_to_json(y_test, y_pred, y_probs, output_file='results.json')

    fpr, tpr, thresholds = roc_curve(y_test, y_probs,
                                     pos_label=1)

    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()

    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.show()

    print("classification_report")
    print(classification_report(y_test, y_pred))