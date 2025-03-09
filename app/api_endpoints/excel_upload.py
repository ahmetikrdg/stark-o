import os
import pandas as pd
import threading

from flask import jsonify, Blueprint, request
from app.configs.model_config import excel_path

excelUpload = Blueprint('excel-upload', __name__)


def save_to_excel(comments, labels):
    try:
        if os.path.exists(excel_path):
            try:
                train_data = pd.read_excel(excel_path, sheet_name='Train Data')
            except ValueError:
                train_data = pd.DataFrame(columns=['text', 'labels'])
        else:
            train_data = pd.DataFrame(columns=['text', 'labels'])

        new_data = pd.DataFrame({"text": comments, "labels": labels})
        train_data = pd.concat([train_data, new_data], ignore_index=True)

        with pd.ExcelWriter(excel_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            train_data.to_excel(writer, sheet_name='Train Data', index=False)

    except Exception as e:
        print(f"Excel kaydetme hatası: {e}")


@excelUpload.route('/excel-upload', methods=['POST'])
def excel_upload():
    try:
        data = request.get_json(force=True)
        comments = data.get("comments", [])
        labels = data.get("labels", [])

        if not isinstance(comments, list) or not isinstance(labels, list):
            return jsonify({"error": "'comments' and 'labels' must be lists."}), 400

        if len(comments) != len(labels):
            return jsonify({"error": "'comments' and 'labels' must have the same length."}), 400

        if len(comments) == 0:
            return jsonify({"error": "At least one comment and label must be provided."}), 400

        thread = threading.Thread(target=save_to_excel, args=(comments, labels))
        thread.start()

        return jsonify({
            "message": "Data insertion process has started. This operation may take some time, please do not shut "
                       "down the system."
        }), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 500
