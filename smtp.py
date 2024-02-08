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


def prepare_mail_enter_event(data):
    vorname = data[0]
    nachname = data[1]
    email = data[2]
    datum_Event = data[3].strftime("%Y-%m-%d %H:%M")
    sport = data[4]
    duration = data[5]
    vorname_creator = data[6]
    nachname_creator = data[7]

    subject = "Vielen Dank für Ihre Teilnahme am Event"
    body = f"""Sehr geehrte/r {vorname} {nachname},

    Vielen Dank, dass Sie sich für das Event am {datum_Event} angemeldet haben. Wir freuen uns, Sie dabei zu haben!

    Hier sind die Details zum Event:
    - Sportart: {sport}
    - Datum und Uhrzeit: {datum_Event}
    - Dauer: {duration} Stunden

    Das Event wurde von {vorname_creator} {nachname_creator} organisiert.

    Bei Fragen stehen wir Ihnen gerne zur Verfügung.

    Mit freundlichen Grüßen,
    [SportSpot]"""

    print(body)
    print(subject)
    print(email)

    return email, subject, body

def prepare_mail_leave_event(data):
    vorname = data[0]
    nachname = data[1]
    email = data[2]
    datum_Event = data[3].strftime("%Y-%m-%d %H:%M")
    sport = data[4]
    duration = data[5]
    vorname_creator = data[6]
    nachname_creator = data[7]

    subject = "Schade, dass Sie nicht teilnehmen konnten"

    body = f"""Sehr geehrte/r {vorname} {nachname},

    wir haben Ihre Abmeldung vom Event am {datum_Event} zur Kenntnis genommen und bedauern zutiefst, dass Sie nicht teilnehmen konnten.

    Event-Details, die Sie verpasst haben:
    - Sportart: {sport}
    - Datum und Uhrzeit: {datum_Event}
    - Geplante Dauer: {duration} Stunden

    Organisiert wurde das Event von {vorname_creator} {nachname_creator}, der/die sicherlich ein unvergessliches Erlebnis geplant hatte.

    Ihre Gesundheit und Ihr Wohlbefinden haben für uns oberste Priorität, und wir verstehen, dass unvorhergesehene Umstände Ihre Pläne ändern können.

    Wir hoffen, Sie bald bei einem unserer zukünftigen Events begrüßen zu dürfen und wünschen Ihnen bis dahin alles Gute.

    Mit freundlichen Grüßen,
    [SportSpot]"""


    print(body)
    print(subject)
    print(email)

    return email, subject, body
