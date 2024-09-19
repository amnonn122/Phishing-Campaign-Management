from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS

from back.dbConnect import getMessageAndEmployeeData, setDB
from back.sendEmail import send_emails_to_employees

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


# Messages collection
messages_collection = db['messages']


# Add a new message (POST)
@app.route('/messages', methods=['POST'])
def add_message():
    data = request.json  # JSON data from the request
    title = data.get('title')
    content = data.get('content')
    message_type = data.get('message_type')

    # Insert the message into the 'messages' collection
    messages_collection.insert_one({
        "title": title,
        "content_template": content,
        "message_type": message_type
    })

    return jsonify({"message": "Message added successfully"}), 201


# Add a route to fetch message types (GET)
@app.route('/message-types', methods=['GET'])
def get_message_types():
    message_types = messages_collection.distinct('message_type')  # Fetch distinct message types from the DB
    return jsonify(message_types), 200


@app.route('/send-emails', methods=['POST'])
def send_emails():
    try:
        data = request.json
        print (data)

        user_names = data['user_names']
        message_types = data['message_types']
        print (message_types)
        # Retrieve message_data and employee_data
        message_data, employee_data = getMessageAndEmployeeData(user_names, message_types)

        # Retrieve email credentials from environment or config (for example)
        from_email = "bguminiproject@gmail.com"
        password = "aoamngkprfukvoif"

        # Send emails to employees
        send_emails_to_employees(message_data, employee_data, from_email, password)

        return jsonify({"success": True}), 200
    except Exception as e:
        print(f"Error while sending emails: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    employees = [
        ["Bar Shuv", "barsh2001@gmail.com"],
    ]

    messages = [
        ("aa55aa", lambda name: f"sdgdfhgfh {name}.", "fish55")
    ]
    setDB(employees, messages)
    app.run(debug=True)
