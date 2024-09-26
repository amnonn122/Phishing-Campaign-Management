from flask import Flask, jsonify, request, redirect
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS
from configIp import ipv4_address

from dbConnect import get_message_and_employee_data, set_DB
from sendEmail import send_emails_to_employees

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['companyDB']
employees_collection = db['employees']
messages_collection = db['messages']

@app.route('/get-ip', methods=['GET'])
def get_ip():
    """
    API route that returns the server's IPv4 address.

    Returns:
        Response: A JSON object with the server's IPv4 address.
    """
    return jsonify({"ipv4": ipv4_address}), 200

@app.route('/employees', methods=['GET'])
def get_employees():
    """
    API route to retrieve all employees from the MongoDB database.

    Returns:
        Response: A JSON array containing all employee records.
    """
    employees = employees_collection.find()
    return dumps(employees)

@app.route('/employees', methods=['POST'])
def add_employee():
    """
    API route to add a new employee to the MongoDB database.

    Expected request body (JSON):
        {
            "name": "Employee Name",
            "email": "Employee Email"
        }

    Returns:
        Response: A message indicating whether the employee was added successfully.
    """
    data = request.json
    name = data.get('name')
    email = data.get('email')
    employees_collection.insert_one({"name": name, "email": email, "phishing_count": 0})
    return jsonify({"message": "Employee added successfully"}), 201

@app.route('/employees/<name>/reset-phishing-count', methods=['PATCH'])
def reset_phishing_count(name):
    """
    API route to reset the phishing count of a specific employee to zero.

    Parameters:
        name (str): The name of the employee to update.

    Returns:
        Response: A message indicating whether the phishing count was reset.
    """
    result = employees_collection.update_one({"name": name}, {"$set": {"phishing_count": 0}})
    if result.matched_count:
        return jsonify({"message": f"Phishing count reset to 0 for {name}"}), 200
    else:
        return jsonify({"message": f"Employee {name} not found"}), 404

@app.route('/employees/<name>/increment', methods=['PATCH'])
def increment_phishing_count(name):
    """
    API route to increment the phishing count of a specific employee.

    Parameters:
        name (str): The name of the employee to update.

    Returns:
        Response: A message indicating whether the phishing count was incremented.
    """
    result = employees_collection.update_one({"name": name}, {"$inc": {"phishing_count": 1}})
    if result.matched_count:
        return jsonify({"message": f"Incremented phishing count for {name}"}), 200
    else:
        return jsonify({"message": f"Employee {name} not found"}), 404

@app.route('/messages', methods=['POST'])
def add_message():
    """
    API route to add a new message template to the MongoDB database.

    Expected request body (JSON):
        {
            "title": "Message Title",
            "content": "Message Content",
            "message_type": "Message Type"
        }

    Returns:
        Response: A message indicating whether the message was added successfully.
    """
    data = request.json
    title = data.get('title')
    content = data.get('content')
    message_type = data.get('message_type')
    messages_collection.insert_one({
        "title": title,
        "content_template": content,
        "message_type": message_type
    })
    return jsonify({"message": "Message added successfully"}), 201

@app.route('/message-types', methods=['GET'])
def get_message_types():
    """
    API route to fetch distinct message types from the database.

    Returns:
        Response: A JSON array containing all distinct message types.
    """
    message_types = messages_collection.distinct('message_type')
    return jsonify(message_types), 200

@app.route('/send-emails', methods=['POST'])
def send_emails():
    """
    API route to send emails to employees based on their names and message types.

    Expected request body (JSON):
        {
            "user_names": ["Employee1", "Employee2"],
            "message_types": ["urgent_update", "account_verification"]
        }

    Returns:
        Response: A message indicating whether the emails were sent successfully.
    """
    try:
        data = request.json
        user_names = data['user_names']
        message_types = data['message_types']

        # Retrieve message and employee data
        message_data, employee_data = get_message_and_employee_data(user_names, message_types)

        # Validate that data exists before sending emails
        if not message_data[0] or not message_data[1]:
            raise ValueError("Message data is incomplete. Titles or contents are missing.")
        if not employee_data:
            raise ValueError("No employee data found.")

        # Send emails
        send_emails_to_employees(message_data[0], message_data[1], employee_data)

        return jsonify({"success": True}), 200
    except Exception as e:
        print(f"Error while sending emails: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/send-warning-email', methods=['POST'])
def send_warning_email():
    """
    API route to send a warning email to an employee.

    Expected request body (JSON):
        {
            "email": "Employee Email",
            "name": "Employee Name"
        }

    Returns:
        Response: A message indicating whether the email was sent successfully.
    """
    try:
        data = request.json
        
        email = data.get('email')
        name = data.get('name')

        if not email or not name: 
            return jsonify({"success": False, "error": "Email and name are required"}), 400
        
        subject = "Warning: Phishing Attempt Detected"
        content = f"Dear {name},<br>You have fallen for a phishing attempt. <br>Please be cautious in the future! <br>Best regards,<br>Your Security Team"
        
        # Sending the warning email using the existing function
        send_emails_to_employees([subject], [content], [{'name': name, 'email': email}])
        
        return jsonify({"success": True, "message": "Warning email sent successfully!"}), 200
    except Exception as e:
        print(f"Error while sending warning email: {e}")
        return jsonify({"success": False, "error": str(e)}), 500



@app.route('/phishing-click', methods=['GET'])
def handle_phishing_click():
    """
    API route to handle a phishing click simulation. This route increments the phishing count for the
    employee who clicked the link and redirects to an external website (YouTube).

    Query parameters:
        email (str): The email of the employee who clicked the phishing link.

    Returns:
        Response: A redirect to YouTube or an error message.
    """
    email = request.args.get('email')
    
    if email and email != "{email}":  # Check if it's not the placeholder
        # Check if the employee exists
        employee = employees_collection.find_one({"email": email})
        
        if employee:
            employees_collection.update_one({"email": email}, {"$inc": {"phishing_count": 1}})
            
            # Redirect to YouTube
            return redirect("https://www.youtube.com")
        else:
            return jsonify({"message": "Employee not found"}), 404
    else:
        return jsonify({"message": "Email parameter is missing or incorrect"}), 400

if __name__ == '__main__':
    # Initializing the database
    employees = [
        ["Israel Israeli", "israel@israel.com"],
    ]

    messages = [
        ("Urgent: Update Your Information", 
        "Hi {name},<br>Please click <a href='{phishing_url}{email}'>HERE</a> to update your information as soon as possible!<br>Best regards,<br>Your Security Team", 
        "urgent_update"),
        
        ("Account Verification", 
        "Hello {name},<br>Please verify your account by clicking <a href='{phishing_url}{email}'>HERE</a>.<br>Best regards,<br>Your Security Team", 
        "account_verification"),
        
        ("Congratulations: You've Won!", 
        "Congratulations {name}!<br>You've won our prize. Click <a href='{phishing_url}{email}'>HERE</a> to claim your prize.<br>Best regards,<br>Your Security Team", 
        "prize_claim"),
        
        ("Warning: Account Issue", 
        "Hello {name},<br>There is an issue with your account. Click <a href='{phishing_url}{email}'>HERE</a> to resolve it.<br>Best regards,<br>Your Security Team", 
        "account_issue"),
        
        ("Invitation to Upgrade Your Account", 
        "Hi {name},<br>We are offering an upgrade for your account. Click <a href='{phishing_url}{email}'>HERE</a> for more information.<br>Best regards,<br>Your Security Team", 
        "account_upgrade"),
    ]
    set_DB(employees, messages)

    app.run(host='0.0.0.0', port=5000, debug=True)