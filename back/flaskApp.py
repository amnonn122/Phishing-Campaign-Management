from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connecting to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['companyDB']
employees_collection = db['employees']

# Retrieve all employees (GET)
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = employees_collection.find()
    return dumps(employees)

# Add a new employee (POST)
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json  # JSON data from the request
    name = data.get('name')
    email = data.get('email')
    employees_collection.insert_one({"name": name, "email": email, "phishing_count": 0})
    return jsonify({"message": "Employee added successfully"}), 201

# Increment phishing_count (PATCH)
@app.route('/employees/<name>/increment', methods=['PATCH'])
def increment_phishing_count(name):
    result = employees_collection.update_one({"name": name}, {"$inc": {"phishing_count": 1}})
    if result.matched_count:
        return jsonify({"message": f"Incremented phishing count for {name}"}), 200
    else:
        return jsonify({"message": f"Employee {name} not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
