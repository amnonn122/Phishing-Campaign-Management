import time

from back.sendEmail import send_emails_to_employees
from dbConnect import setDB, addEmployee, increment_phishing_count, getMessagesForEmployees

from_email = "bguminiproject@gmail.com"
password = "aoamngkprfukvoif"
employees = [
    [ "Bar Shuv" ,"barsh2001@gmail.com"],
    ["Amnon Abaev", "amnonn122@gmail.com"]
]
messages = [
    ("Welcome", lambda name: f""""
<html>
<head></head>
<body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
        <h2 style="color: red;"> {name} Warning: Your Account Has Been Compromised!</h2>
        <p>Hello,</p>
        <p>We have detected suspicious activity on your account. To secure your account, please <a href="http://malicious-link.com" style="color: blue;">click here</a> and update your login details immediately.</p>
        <p style="color: red; font-weight: bold;">Failure to do so will result in a suspension of your account!</p>
        <p style="font-size: 12px; color: grey;">Thank you, <br> The Support Team</p>
        <hr style="border: none; border-top: 1px solid #eee;"/>
        <p style="font-size: 10px; color: grey;">This is an automated message. Please do not reply.</p>
    </div>
</body>
</html>
""" ),

    ("Alert", lambda name: f"Please be cautious of phishing attempts, {name}.")
]

employee_names = ["Bar Shuv"]

setDB(employees, messages)
send_emails_to_employees(employee_names, from_email, password)



try:
    while True:
        print("MongoDB server is running. Press Ctrl+C to stop.")
        time.sleep(60)  # Sleep for 60 seconds before the next print








except KeyboardInterrupt:
    print("Shutting down the server...")