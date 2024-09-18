#
# # HTML phishing-style email body
# import sendEmail
#
# html_body = """
# <html>
# <head></head>
# <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
#     <div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
#         <h2 style="color: red;">Warning: Your Account Has Been Compromised!</h2>
#         <p>Hello,</p>
#         <p>We have detected suspicious activity on your account. To secure your account, please <a href="http://malicious-link.com" style="color: blue;">click here</a> and update your login details immediately.</p>
#         <p style="color: red; font-weight: bold;">Failure to do so will result in a suspension of your account!</p>
#         <p style="font-size: 12px; color: grey;">Thank you, <br> The Support Team</p>
#         <hr style="border: none; border-top: 1px solid #eee;"/>
#         <p style="font-size: 10px; color: grey;">This is an automated message. Please do not reply.</p>
#     </div>
# </body>
# </html>
# """
#
# # Using the function to send emails
# from_email = "bguminiproject@gmail.com"
# password = "aoamngkprfukvoif"
# email_list = ["barsh2001@gmail.com", "amnonn122@gmail.com"]
# subject = "Urgent: Action Required to Secure Your Account!"
#
# sendEmail.send_email_to_list(from_email, password, email_list, subject, html_body)
#
#
#




from dbConnect import setDB

# Example usage
employees = [
    ["Bar Shuv", "barsh2001@gmail.com"],
    ["Amnon Abaev", "amnonn122@gmail.com"]
]

setDB(employees)
