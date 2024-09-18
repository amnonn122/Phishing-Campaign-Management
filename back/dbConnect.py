from pymongo import MongoClient


def connect_db():
    """
    Connect to MongoDB and return the collections for 'employees' and 'messages'.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client['companyDB']
    employees_collection = db['employees']
    messages_collection = db['messages']
    return employees_collection, messages_collection


def addEmployee(name, email):
    """
    Add an employee to the MongoDB database.

    Parameters:
    name (str): The name of the employee.
    email (str): The email of the employee.
    """
    collection = connect_db()
    # Insert the employee record into the collection with phishing_count initialized to 0
    result = collection.insert_one({"name": name, "email": email, "phishing_count": 0})
    return result.inserted_id


def setDB(employee_data, message_data):
    """
    Initialize the MongoDB database with employee data and message types.

    Parameters:
    employee_data (list of list): A 2D array where each inner list contains
                                  two strings: employee name and email.
    message_data (list of tuple): A list of tuples where each tuple contains
                                   the message title and a function that generates the content.
    """
    # Step 1: Connect to MongoDB (assuming it's running locally)
    client = MongoClient("mongodb://localhost:27017/")

    # Step 2: Create or connect to the 'companyDB' database
    db = client['companyDB']

    # Step 3: Create or connect to the 'employees' collection
    employee_collection = db['employees']

    # Step 4: Clear any existing data in the 'employees' collection (optional)
    employee_collection.delete_many({})

    # Step 5: Prepare and insert employee data into MongoDB with phishing_count initialized to 0
    employee_records = []
    for name, email in employee_data:
        employee_records.append({"name": name, "email": email, "phishing_count": 0})

    # Step 6: Insert the records into the 'employees' collection
    employee_collection.insert_many(employee_records)
    print(f"Inserted {len(employee_records)} employee records into the 'employees' collection.")

    # Step 7: Create or connect to the 'messages' collection
    message_collection = db['messages']

    # Step 8: Clear any existing data in the 'messages' collection (optional)
    message_collection.delete_many({})

    # Step 9: Prepare and insert message data into MongoDB
    message_records = []
    for title, content_function in message_data:
        for name, _ in employee_data:
            content = content_function(name)  # Pass employee name to the content function
            message_records.append({"title": title, "content": content})

    # Step 10: Insert the records into the 'messages' collection
    message_collection.insert_many(message_records)
    print(f"Inserted {len(message_records)} message records into the 'messages' collection.")


def increment_phishing_count(name):
    """
    Increment the phishing count for a user by 1.

    Parameters:
    name (str): The name of the employee.
    """
    collection = connect_db()
    # Increment the phishing_count field for the specified employee
    result = collection.update_one(
        {"name": name},
        {"$inc": {"phishing_count": 1}}
    )
    if result.matched_count:
        print(f"Incremented phishing count for {name}.")
    else:
        print(f"No employee found with name {name}.")


def get_names_by_phishing_count():
    """
    Return a 2D array of employee names and their phishing counts in descending order.

    Returns:
    list of lists: A 2D array where each inner list contains the employee's name and phishing count.
    """
    collection = connect_db()

    # Query the collection to find all employees, sorted by phishing_count in descending order
    cursor = collection.find({}).sort("phishing_count", -1)

    # Prepare a 2D array to store names and phishing counts
    result = []

    # Add each employee's name and phishing count to the 2D array
    for employee in cursor:
        name = employee.get("name")
        phishing_count = employee.get("phishing_count")
        result.append([name, phishing_count])

    return result


def getMessagesForEmployees(employee_names):
    """
    Retrieve personalized messages for a list of employees.

    Parameters:
    employee_names (list of str): A list of employee names to retrieve messages for.

    Returns:
    list of lists: A 2D array where each inner list contains an employee's name
                    and a list of personalized messages for that employee.
    """
    # Step 1: Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client['companyDB']

    # Step 2: Access the 'messages' collection
    message_collection = db['messages']

    # Step 3: Prepare a result list
    result = []

    # Step 4: Retrieve and personalize messages for each employee
    for employee_name in employee_names:
        # Query all messages
        messages = message_collection.find()
        personalized_messages = []

        for message in messages:
            title = message.get("title")
            content = message.get("content")

            # Replace placeholder with employee's name
            personalized_content = content.replace("{name}", employee_name)
            personalized_messages.append({"title": title, "content": personalized_content})

        result.append([employee_name, personalized_messages])

    return result
