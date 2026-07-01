import smtplib
import ssl
import csv
import os
import time
import logging
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import schedule 


logging.basicConfig(
    filename="email_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class ConfigLoader:
    def __init__(self):
        # In production, pull these from environment variables instead
        # of hardcoding them, e.g. os.environ.get("EMAIL_PASSWORD")
        self.smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("SMTP_PORT", 587))
        self.sender_email = os.environ.get("SENDER_EMAIL", "gurralarohithkumar@gmail.com")
        self.sender_password = os.environ.get("SENDER_PASSWORD", "uqxo deux glqm vrsn")


class RecipientManager:

    def __init__(self, csv_path):
        self.csv_path = csv_path

    def get_recipients(self):
        recipients = []
        with open(self.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                recipients.append({
                    "name": row.get("name", "").strip(),
                    "email": row.get("email", "").strip(),
                    "attachment": row.get("attachment", "").strip(),
                    "image": row.get("image", "").strip(),
                    "schedule": row.get("schedule", "").strip(),
                    "sent": False
                })
        return recipients

class EmailComposer:

    def __init__(self, subject_template, body_template, image_path=None):
        self.subject_template = subject_template
        self.body_template = body_template
        self.image_path = image_path

    def compose(self, sender_email, recipient):

        msg = MIMEMultipart("related")

        msg["From"] = sender_email
        msg["To"] = recipient["email"]
        msg["Subject"] = self.subject_template.format(name=recipient["name"])

        body = f"""
        <html>
        <body>
            <p>{self.body_template.format(name=recipient['name'] or 'there')}</p>

            <img src="cid:companylogo" width="400">

            <p><br>Regards,<br>Team</p>
        </body>
        </html>
        """

        msg.attach(MIMEText(body, "html"))

        if self.image_path and os.path.isfile(self.image_path):

            with open(self.image_path, "rb") as img:

                image = MIMEImage(img.read())

                image.add_header("Content-ID", "<companylogo>")

                image.add_header(
                    "Content-Disposition",
                    "inline",
                    filename=os.path.basename(self.image_path)
                )

                msg.attach(image)

        return msg

class AttachmentHandler:

    @staticmethod
    def attach_file(msg, file_path):

        if not file_path:
            return msg
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, file_path)
        if not os.path.isfile(file_path):
            print(f"Attachment not found: {file_path}")
            return msg
        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{os.path.basename(file_path)}"'
        )
        msg.attach(part)
        return msg

class SMTPConnection:

    def __init__(self, config: ConfigLoader):
        self.config = config
        self.server = None

    def connect(self):
        context = ssl.create_default_context()
        self.server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
        self.server.ehlo()
        self.server.starttls(context=context)
        self.server.ehlo()
        self.server.login(self.config.sender_email, self.config.sender_password)

    def send(self, msg):
        try:
            self.server.sendmail(msg["From"], msg["To"], msg.as_string())
            logging.info(f"Email sent successfully to {msg['To']}")
            return True
        except Exception as e:
            logging.error(f"Failed to send email to {msg['To']}: {e}")
            return False

    def close(self):
        if self.server:
            self.server.quit()


def run_email_batch(csv_path, subject_template, body_template):
    config = ConfigLoader()
    recipient_manager = RecipientManager(csv_path)
    composer = EmailComposer(
    subject_template,
    body_template,
    image_path="images/images.jpeg")
    connection = SMTPConnection(config)

    recipients = recipient_manager.get_recipients()
    if not recipients:
        logging.warning("No recipients found in dataset.")
        return

    connection.connect()

    success_count = 0
    fail_count = 0

    for recipient in recipients:
        if not recipient["email"]:
            continue

        msg = composer.compose(config.sender_email, recipient)
        msg = AttachmentHandler.attach_file(msg, recipient.get("attachment"))

        sent = connection.send(msg)
        if sent:
            success_count += 1
        else:
            fail_count += 1

    connection.close()

    summary = f"Batch complete: {success_count} sent, {fail_count} failed at {datetime.now()}"
    print(summary)
    logging.info(summary)


def start_scheduler(csv_path, subject_template, body_template):
    config = ConfigLoader()
    recipient_manager = RecipientManager(csv_path)
    composer = EmailComposer(
        subject_template,
        body_template,
        image_path="images/images.jpeg"
    )
    recipients = recipient_manager.get_recipients()

    print("Scheduler Started...")

    while True:
        current_time = datetime.now().strftime("%H:%M")
        for recipient in recipients:
            if recipient["sent"]:
                continue
            if recipient["schedule"] == current_time:
                print(f"Sending email to {recipient['name']}...")
                connection = SMTPConnection(config)
                connection.connect()
                msg = composer.compose(config.sender_email, recipient)
                msg = AttachmentHandler.attach_file(
                    msg,
                    recipient.get("attachment")
                )
                connection.send(msg)
                connection.close()
                recipient["sent"] = True
        time.sleep(30)


if __name__ == "__main__":
    CSV_PATH = "recipients.csv"        
    SUBJECT = "Reminder for {name}"
    BODY = "Hi {name},\n\nThis is an automated reminder from our system.\n\nRegards,\nTeam"
    start_scheduler(
    CSV_PATH,
    SUBJECT,
    BODY
)
    