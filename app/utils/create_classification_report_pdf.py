import io
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import classification_report, confusion_matrix


def create_classification_report_pdf(y_test, y_pred, y_probs):
    with io.BytesIO() as buffer:
        with PdfPages(buffer) as pdf:
            fpr, tpr, _ = roc_curve(y_test, y_probs, pos_label=1)
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
            pdf.savefig()
            plt.close()

            cm = confusion_matrix(y_test, y_pred)
            plt.figure(figsize=(8, 6))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
            plt.title('Confusion Matrix')
            plt.xlabel('Predicted Labels')
            plt.ylabel('True Labels')
            pdf.savefig()
            plt.close()
            plt.show()

            report = classification_report(y_test, y_pred)
            plt.figure(figsize=(8.5, 11))
            plt.text(0.01, 0.99, report, {'fontsize': 10}, fontproperties='monospace', verticalalignment='top')
            plt.axis('off')
            plt.title('Classification Report')
            pdf.savefig()
            plt.close()

        buffer.seek(0)
        return buffer.read()
