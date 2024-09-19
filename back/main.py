import time

from back.sendEmail import send_emails_to_employees
from dbConnect import setDB, addEmployee, increment_phishing_count, getMessagesForEmployees, getMessageAndEmployeeData
#    ["Amnon Abaev", "amnonn122@gmail.com"]

from_email = "bguminiproject@gmail.com"
password = "aoamngkprfukvoif"
employees = [
    [ "Bar Shuv" ,"barsh2001@gmail.com"],
]

messages = [
    ("Alert", lambda name: f"Please be cautious of phishing attempts, {name}.","fish2")
]
setDB(employees, messages)



# Example usage
user_names = ["Bar Shuv", "Amnon Abaev"]
message_types = ["fish2"]

message_data, employee_data = getMessageAndEmployeeData(user_names, message_types)
#send_emails_to_employees(message_data, employee_data, from_email, password)
