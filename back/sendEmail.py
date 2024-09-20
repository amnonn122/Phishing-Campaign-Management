import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
def send_emails_to_employees(title, content, employee_data, from_email, password):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Encrypt connection
        server.login(from_email, password)

        for name, email in employee_data:
            # Replace {name} in the content with the actual employee name
            personalized_content = content.replace("{name}", name).replace("{email}", email)

            send_email_to_one(server, from_email, email, title, personalized_content)

        server.quit()
    except Exception as e:
        print(f"Error while sending emails: {e}")