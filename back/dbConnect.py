from pymongo import MongoClient
from sendEmail import get_from_email

def set_DB(employee_data, message_data):
    """
    Initialize the MongoDB database with employee and message data.

    Parameters:
    employee_data (list of list): Each inner list contains employee name and email.
    message_data (list of tuple): Each tuple contains message title, content function, and message type.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client['companyDB']
    employee_collection = db['employees']

    # Clear existing employee data
    employee_collection.delete_many({})

    # Insert employee data with phishing_count initialized to 0
    employee_records = [{"name": name, "email": email, "phishing_count": 0} for name, email in employee_data]
    employee_collection.insert_many(employee_records)
    print(f"Inserted {len(employee_records)} employee records.")

    # Prepare messages collection
    message_collection = db['messages']
    message_collection.delete_many({})  # Clear existing messages

    # Insert message data
    message_records = [{
        "title": title,
        "content_template": content_function("{name}", "{email}", "{phishing_ur}"),
        "message_type": message_type
    } for title, content_function, message_type in message_data]

    message_collection.insert_many(message_records)
    print(f"Inserted {len(message_records)} message records.")

    # Create new clicks collection
    db['clicks']

    # Printing the from email details
    from_email, password = get_from_email()
    print(f"Sending emails from: {from_email}")

def get_message_and_employee_data(user_names, message_types):
    """
    Retrieve messages and employees data from the database.

    Parameters:
        user_names (list): List of employee names to retrieve.
        message_types (list): List of message types to retrieve.

    Returns:
        tuple: Contains two lists:
            - Message titles and content.
            - Corresponding employee data.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client['companyDB']
    employees_collection = db['employees']
    messages_collection = db['messages']

    # Fetch employee details
    employee_data = list(employees_collection.find({"name": {"$in": user_names}}))

    # Fetch messages based on types
    messages_data = list(messages_collection.find({"message_type": {"$in": message_types}}))
    message_titles = [message['title'] for message in messages_data]
    message_contents = [message['content_template'] for message in messages_data]

    return (message_titles, message_contents), employee_data
