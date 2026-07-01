from flask import jsonify, request, abort
from service import app
from service.models import Account, DataValidationError, db

@app.route('/')
def index():
    return jsonify({"name": "Account REST API Service", "version": "1.0"})

@app.route('/health')
def health():
    return jsonify({"status": "OK"}), 200

@app.route('/accounts', methods=['POST'])
def create_accounts():
    data = request.get_json()
    if not data or "name" not in data:
        abort(400, "Missing required fields")
    account = Account()
    account.deserialize(data)
    account.create()
    return jsonify(account.serialize()), 201

@app.route('/accounts', methods=['GET'])
def list_accounts():
    accounts = Account.all()
    return jsonify([a.serialize() for a in accounts]), 200

@app.route('/accounts/<int:account_id>', methods=['GET'])
def get_accounts(account_id):
    account = Account.find(account_id)
    if not account:
        abort(404, "Account not found")
    return jsonify(account.serialize()), 200

@app.route('/accounts/<int:account_id>', methods=['PUT'])
def update_accounts(account_id):
    account = Account.find(account_id)
    if not account:
        abort(404, "Account not found")
    data = request.get_json()
    account.deserialize(data)
    account.update()
    return jsonify(account.serialize()), 200

@app.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_accounts(account_id):
    account = Account.find(account_id)
    if not account:
        abort(404, "Account not found")
    account.delete()
    return jsonify({"message": "Account deleted"}), 204
