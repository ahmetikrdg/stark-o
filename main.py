import json
import os

from flask import Flask

from app.models.model_load import modelLoad
from app.models.model_start import modelStart

from app.api_endpoints.set_start_model import setStartModel
from app.api_endpoints.generate_report import generateReport
from app.api_endpoints.excel_upload import excelUpload
from app.api_endpoints.analyze_comment import analyzeComment

app = Flask(__name__)


def check_files_existence(files):
    return all(os.path.exists(file) for file in files)


with open('config.json', 'r') as file:
    config = json.load(file)

if __name__ == '__main__':
    if config.get('startModel'):
        modelStart()
    else:
        modelLoad()

    app.register_blueprint(setStartModel)
    app.register_blueprint(generateReport)
    app.register_blueprint(excelUpload)
    app.register_blueprint(analyzeComment)

    app.run(port=6666)
