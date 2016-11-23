from flask import Flask, jsonify, request
from return_json import return_schema

app = Flask(__name__)


@app.route('/get')
def get():
    response = return_schema
    return jsonify(**response)


@app.route('/remove')
def decline():
    sub_id = request.args.get('subscriptionId')

    response = {
        "meta": {
            "status": "OK",
            "code": 20000,
            "message": None,
            "id": sub_id
        }
    }
    return jsonify(**response)


if __name__ == "__main__":
    app.run(port=5050, debug=True)