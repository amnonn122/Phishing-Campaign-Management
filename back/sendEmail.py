import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from configIp import ipv4_address

# The phising URL that will be in the messages
phishing_url = f"http://{ipv4_address}:5000/phishing-click?email="

def get_from_email():
    """
    Reads the email details from a text file in the main directory.

    Returns:
        tuple: (from_email, password) read from the file.
    """
    credentials_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fromEmailDetails.txt')
    
    with open(credentials_path, 'r') as file:
        lines = file.readlines()
        from_email = lines[0].split(':')[1].strip()  # email in the first line
        password = lines[1].split(':')[1].strip()    # password in the second line
    return from_email, password

import os

def get_smtp_details():
    """
    Reads the SMTP server and port details from a text file in the main directory.

    Returns:
        tuple: (smtp_server, smtp_port) read from the file.
    """
    credentials_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fromEmailDetails.txt')
    
    with open(credentials_path, 'r') as file:
        lines = file.readlines()
        smtp_server = lines[2].split(':')[1].strip()  # SMTP server in the 3 line
        smtp_port = int(lines[3].split(':')[1].strip())  # SMTP port in the 4 line
    return smtp_server, smtp_port


def send_emails_to_employees(subjects, contents, employees):
    """
    Sends emails to employees with the given subjects and contents in HTML format.

    Parameters:
        subjects (list): A list of email subjects to send.
        contents (list): A list of email bodies to send (in HTML format).
        employees (list): A list of employee dictionaries, each containing 'name' and 'email'.

    Returns:
        None
    """
    # Getting the SMTP server and port details
    smtp_server, smtp_port = get_smtp_details()

    # Getting the from_email details
    from_email, password = get_from_email()

    # Create SMTP session
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Enable security
    server.login(from_email, password)

    for subject, content in zip(subjects, contents):
        for employee in employees:
            name = employee['name']
            to_email = employee['email']

            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject

            # Replace placeholders in content
            personalized_content = content.replace("{name}", name).replace("{email}", to_email).replace("{phishing_url}", phishing_url)

            # Attach the personalized content as HTML
            msg.attach(MIMEText(personalized_content, 'html'))

            # Send the email
            try:
                server.sendmail(from_email, to_email, msg.as_string())
                print(f"Email sent to {name} at {to_email}")
            except Exception as e:
                print(f"Failed to send email to {name} at {to_email}: {e}")

    # Terminate the SMTP session
    server.quit()