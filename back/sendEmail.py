import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from back.dbConnect import getMessagesForEmployees, connect_db


# Function to email a single recipient
def send_email_to_one(server, from_email, to_email, subject, body):
    try:
        # Ensure the body is a string
        if isinstance(body, list):
            body = ''.join(body)  # Convert list to string if needed
        elif not isinstance(body, str):
            body = str(body)  # Ensure body is always a string

        # Create MIME object
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the email body in HTML format
        msg.attach(MIMEText(body, 'html'))

        # Send the email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)

        print(f"Email sent successfully to {to_email}!")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")


# Send emails to a list of employees with personalized messages
def send_emails_to_employees(employee_names, from_email, password):
    try:
        # Connect to Gmail server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Encrypt connection

        # Login with the given email and password
        server.login(from_email, password)

        # Fetch employees and messages collections from MongoDB
        employees_collection, messages_collection = connect_db()

        # Send an email to each employee with their personalized message
        for name in employee_names:
            # Fetch employee details
            employee = employees_collection.find_one({"name": name})
            if not employee:
                print(f"Employee '{name}' not found in the database.")
                continue

            employee_email = employee.get("email")

            # Fetch all messages from the database
            messages = messages_collection.find()

            for message in messages:
                title = message.get("title")
                content = message.get("content").replace("{name}", name)  # Personalize the content

                # Send the personalized email
                send_email_to_one(server, from_email, employee_email, title, content)

        # Disconnect from the server after all emails are sent
        server.quit()

    except Exception as e:
        print(f"Failed to connect to the server. Error: {e}")