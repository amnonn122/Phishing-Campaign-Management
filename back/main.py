import time

from back.sendEmail import send_emails_to_employees
from dbConnect import setDB, addEmployee, increment_phishing_count, getMessagesForEmployees, getMessageAndEmployeeData

from_email = "bguminiproject@gmail.com"
password = "aoamngkprfukvoif"
employees = [
    [ "Bar Shuv" ,"barsh2001@gmail.com"],
    ["Amnon Abaev", "amnonn122@gmail.com"]
]
messages = [
    ("Alert", lambda name: f"Please be cautious of phishing attempts, {name}.","fish2")
]
setDB(employees, messages)



# Example usage
user_names = ["Bar Shuv", "Amnon Abaev"]
message_types = ["fish2"]

message_data, employee_data = getMessageAndEmployeeData(user_names, message_types)
send_emails_to_employees(message_data, employee_data, from_email, password)



try:
    while True:
        print("MongoDB server is running. Press Ctrl+C to stop.")
        time.sleep(60)  # Sleep for 60 seconds before the next print








except KeyboardInterrupt:
    print("Shutting down the server...")