import json

from flask import request, jsonify, Blueprint

setStartModel = Blueprint('set-start-model', __name__)


@setStartModel.route('/set-start-model', methods=['POST'])
def set_start_model():
    try:
        data = request.get_json(force=True)
        new_value = data.get("startModel")

        if new_value is None or not isinstance(new_value, bool):
            return jsonify({"error": "startModel must be a boolean value."}), 400

        with open('config.json', 'r') as file:
            config = json.load(file)

        config["startModel"] = new_value

        with open('config.json', 'w') as file:
            json.dump(config, file, indent=4)

        return jsonify({
            "message": "Configuration updated successfully.",
            "startModel": new_value
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
