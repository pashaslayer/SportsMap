import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sender and recipient email addresses
sender_email = "your@email.com"

# SMTP server configuration
smtp_server = "your.smtp.server"
smtp_port = 999  # For SSL, use 465
smtp_user = "your@useremail.com"
smtp_password = "yourpassword"



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

def convert_sport_id_to_string(number):
    sport_in_string = ""
    if number == 1:
        sport_in_string = "Cycling"
    elif number == 2:
        sport_in_string = "Hiking"
    elif number == 3:
        sport_in_string = "Running"
    elif number == 4:
        sport_in_string = "Skiing"
    elif number == 5:
        sport_in_string = "Weightlifting"
    return sport_in_string

def prepare_mail_enter_event(data):
    vorname = data[0]
    nachname = data[1]
    email = data[2]
    date_event = data[3].strftime("%Y-%m-%d %H:%M")
    sport = convert_sport_id_to_string(int(data[4]))
    duration = data[5]
    vorname_creator = data[6]
    nachname_creator = data[7]

    subject = "Vielen Dank für Ihre Teilnahme am Event"
    body = f"""Sehr geehrte/r {vorname} {nachname},

    Vielen Dank, dass Sie sich für das Event am {date_event} angemeldet haben. Wir freuen uns, Sie dabei zu haben!

    Hier sind die Details zum Event:
    - Sportart: {sport}
    - Datum und Uhrzeit: {date_event}
    - Dauer: {duration} Stunden

    Das Event wurde von {vorname_creator} {nachname_creator} organisiert.

    Bei Fragen stehen wir Ihnen gerne zur Verfügung.

    Mit freundlichen Grüßen,
    [SportsMap]"""

    print(body)
    print(subject)
    print(email)

    return email, subject, body

def prepare_mail_leave_event(data):
    vorname = data[0]
    nachname = data[1]
    email = data[2]
    date_event = data[3].strftime("%Y-%m-%d %H:%M")
    sport = convert_sport_id_to_string(int(data[4]))
    duration = data[5]
    vorname_creator = data[6]
    nachname_creator = data[7]

    subject = "Schade, dass Sie nicht teilnehmen konnten"

    body = f"""Sehr geehrte/r {vorname} {nachname},

    wir haben Ihre Abmeldung vom Event am {date_event} zur Kenntnis genommen und bedauern zutiefst, dass Sie nicht teilnehmen konnten.

    Event-Details, die Sie verpasst haben:
    - Sportart: {sport}
    - Datum und Uhrzeit: {date_event}
    - Geplante Dauer: {duration} Stunden

    Organisiert wurde das Event von {vorname_creator} {nachname_creator}, der/die sicherlich ein unvergessliches Erlebnis geplant hatte.

    Ihre Gesundheit und Ihr Wohlbefinden haben für uns oberste Priorität, und wir verstehen, dass unvorhergesehene Umstände Ihre Pläne ändern können.

    Wir hoffen, Sie bald bei einem unserer zukünftigen Events begrüßen zu dürfen und wünschen Ihnen bis dahin alles Gute.

    Mit freundlichen Grüßen,
    [SportsMap]"""


    print(body)
    print(subject)
    print(email)

    return email, subject, body

def prepare_mail_change_event(data, new_date, new_duration):
    
    vorname, nachname, email, sport_id, vorname_creator, nachname_creator = data
    sport = convert_sport_id_to_string(int(sport_id))

    subject = "Wichtige Aktualisierung zu Ihrem bevorstehenden Event"

    body = f"""Sehr geehrte/r {vorname} {nachname},

    wir möchten Sie darüber informieren, dass es Änderungen an einem Event gegeben hat, für das Sie sich angemeldet haben. Bitte überprüfen Sie die aktualisierten Details und lassen Sie uns wissen, ob Sie weiterhin teilnehmen können.

    Aktualisierte Event-Details:
    - Sportart: {sport}
    - Neues Datum und Uhrzeit: {new_date}
    - Geplante Dauer: {new_duration} Stunden

    Die Änderungen wurden von {vorname_creator} {nachname_creator}, dem Organisator des Events, vorgenommen. Wir hoffen, dass die Änderungen für Sie passend sind und freuen uns darauf, Sie beim Event begrüßen zu dürfen.

    Falls Sie Fragen zu den Änderungen haben oder weitere Informationen benötigen, zögern Sie bitte nicht, uns zu kontaktieren.

    Wir danken Ihnen für Ihr Verständnis und Ihre Flexibilität.

    Mit freundlichen Grüßen,
    [SportsMap]"""

    print(body)
    print(subject)
    print(email)

    return email, subject, body