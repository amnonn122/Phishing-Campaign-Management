import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to email a single recipient
def send_email_to_one(server, from_email, to_email, subject, body):
    try:
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

# Function to send emails to a list of recipients using a single server connection
def send_email_to_list(from_email, password, email_list, subject, body):
    try:
        # Connect to Gmail server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Encryption

        # Login with the given email and password
        server.login(from_email, password)

        # Send email to each recipient in the list
        for email in email_list:
            send_email_to_one(server, from_email, email, subject, body)

        # Disconnect from the server after all emails are sent
        server.quit()

    except Exception as e:
        print(f"Failed to connect to the server. Error: {e}")






























