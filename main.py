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

# HTML phishing-style email body
html_body = """
<html>
<head></head>
<body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
        <h2 style="color: red;">Warning: Your Account Has Been Compromised!</h2>
        <p>Hello,</p>
        <p>We have detected suspicious activity on your account. To secure your account, please <a href="http://malicious-link.com" style="color: blue;">click here</a> and update your login details immediately.</p>
        <p style="color: red; font-weight: bold;">Failure to do so will result in a suspension of your account!</p>
        <p style="font-size: 12px; color: grey;">Thank you, <br> The Support Team</p>
        <hr style="border: none; border-top: 1px solid #eee;"/>
        <p style="font-size: 10px; color: grey;">This is an automated message. Please do not reply.</p>
    </div>
</body>
</html>
"""

# Using the function to send emails
from_email = "bguminiproject@gmail.com"
password = "aoamngkprfukvoif"
email_list = ["barsh2001@gmail.com", "amnonn122@gmail.com"]
subject = "Urgent: Action Required to Secure Your Account!"

send_email_to_list(from_email, password, email_list, subject, html_body)
