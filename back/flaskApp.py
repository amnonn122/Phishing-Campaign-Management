from flask import Flask, jsonify, request, redirect
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS
from datetime import datetime

from dbConnect import getMessageAndEmployeeData, setDB
from sendEmail import send_emails_to_employees

app = Flask(__name__)
CORS(app)

phishing_url = "http://10.100.102.17:5000/phishing-click?email=" #CHANGE TO GLOBAL VAR

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
        user_names = data['user_names']
        message_types = data['message_types']

        # Retrieve message_data and employee_data
        message_data, employee_data = getMessageAndEmployeeData(user_names, message_types)

        # Retrieve email credentials from environment or config
        from_email = "bguminiproject@gmail.com"
        password = "aoamngkprfukvoif"

        # Send emails to employees with customized content
        send_emails_to_employees(message_data[0], message_data[1], employee_data, from_email, password)

        return jsonify({"success": True}), 200
    except Exception as e:
        print(f"Error while sending emails: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/phishing-click', methods=['GET'])
def handle_phishing_click():
    email = request.args.get('email')  # Get the email from the query parameters
    
    if email and email != "{email}":  # Make sure it's not the placeholder
        # Check if the email exists in the database
        employee = employees_collection.find_one({"email": email})
        
        if employee:
            # Save the click information in the database
            db['clicks'].insert_one({
                "email": email,
                "timestamp": datetime.now()
            })
            
            # Increment the phishing_count for the employee
            employees_collection.update_one({"email": email}, {"$inc": {"phishing_count": 1}})
            
            # Redirect to YouTube
            return redirect("https://www.youtube.com") 
        else:
            return jsonify({"message": "Employee not found"}), 404
    else:
        return jsonify({"message": "Email parameter is missing or incorrect"}), 400

if __name__ == '__main__':
    employees = [
        ["Amnon Abaev", "amnonn122@gmail.com"],
        ["Yam Peer", "yamitpeer@gmail.com"],
    ]

    messages = [
        ("Urgent: Update Your Information", 
         lambda name, email: f"Hi {name}, please click HERE: <a href='{phishing_url}{email}'>HERE</a> to update your information as soon as possible!", 
         "urgent_update"),
         
        ("Account Verification", 
         lambda name, email: f"Hello {name}, please verify your account by clicking HERE: <a href='{phishing_url}{email}'>HERE</a>.", 
         "account_verification"),
         
        ("Congratulations: You've Won!", 
         lambda name, email: f"Congratulations {name}! You've won our prize. Click HERE: <a href='{phishing_url}{email}'>HERE</a> to claim your prize.", 
         "prize_claim"),
         
        ("Warning: Account Issue", 
         lambda name, email: f"Hello {name}, there is an issue with your account. Click HERE: <a href='{phishing_url}{email}'>HERE</a> to resolve it.", 
         "account_issue"),
         
        ("Invitation to Upgrade Your Account", 
         lambda name, email: f"Hi {name}, we are offering an upgrade for your account. Click HERE: <a href='{phishing_url}{email}'>HERE</a> for more information.", 
         "account_upgrade"),
    ]

    setDB(employees, messages)
    app.run(host='0.0.0.0', port=5000, debug=True)