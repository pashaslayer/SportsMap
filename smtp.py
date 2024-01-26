import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sender and recipient email addresses
sender_email = "sportspotaustria@outlook.com"
receiver_email = "pavel.khakhlou@gmx.at"

# SMTP server configuration
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587  # For SSL, use 465
smtp_user = "sportspotaustria@outlook.com"
smtp_password = ""

# Email content
subject = "Subject"
body = """
Example body
"""

# Setup MIME
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Attach the email body to the MIME message
message.attach(MIMEText(body, "plain"))

# Send the email
try:
    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")