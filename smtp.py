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
smtp_password = "4jGpP5GsQXUF9R9"



def send_mail(to, send_body, send_subject):
    # Email content
    subject = send_subject
    body = send_body
    # Setup MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to
    message["Subject"] = subject

    # Attach the email body to the MIME message
    message.attach(MIMEText(body, "plain"))

    # Send the email
    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, to, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


