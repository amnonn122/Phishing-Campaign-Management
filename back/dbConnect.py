from pymongo import MongoClient

def connect_db():
    """
    Connect to MongoDB and return the collection for 'employees'.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client['companyDB']
    collection = db['employees']
    return collection

def addEmployee(name, email):
    """
    Add an employee to the MongoDB database.

    Parameters:
    name (str): The name of the employee.
    email (str): The email of the employee.
    """
    collection = connect_db()
    # Insert the employee record into the collection
    result = collection.insert_one({"name": name, "email": email})
    return result.inserted_id

def setDB(employee_data):
    """
    Initialize the MongoDB database with employee data.

    Parameters:
    employee_data (list of list): A 2D array where each inner list contains
                                  two strings: employee name and email.
    """
    # Step 1: Connect to MongoDB (assuming it's running locally)
    client = MongoClient("mongodb://localhost:27017/")

    # Step 2: Create or connect to the 'companyDB' database
    db = client['companyDB']

    # Step 3: Create or connect to the 'employees' collection
    collection = db['employees']

    # Step 4: Clear any existing data in the collection (optional)
    # collection.delete_many({})

    # Step 5: Prepare and insert employee data into MongoDB
    employee_records = []
    for employee in employee_data:
        name, email = employee
        employee_records.append({"name": name, "email": email})

    # Step 6: Insert the records into the collection
    collection.insert_many(employee_records)

    # Print a success message
    print(f"Inserted {len(employee_records)} employee records into the database.")

def newa(employee_data):
    print "1"