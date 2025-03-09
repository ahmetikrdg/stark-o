import io

from flask import send_file, Blueprint

from app.utils.create_classification_report_pdf import create_classification_report_pdf
from app.utils.read_json_file import read_json_file

generateReport = Blueprint('generate-report', __name__)


@generateReport.route('/generate-report', methods=['GET'])
def generate_report():
    result = read_json_file("results.json")
    y_test = result.get("y_test")
    y_probs = result.get("y_probs")
    y_pred = result.get("y_pred")

    pdf_content = create_classification_report_pdf(y_test, y_pred, y_probs)

    return send_file(
        io.BytesIO(pdf_content),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='model_report.pdf'
    )
