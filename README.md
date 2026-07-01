# Automated Email Sender

## Overview

Automated Email Sender is a Python-based application that automates the process of sending emails to one or multiple recipients. The application reads recipient details from a CSV file, composes personalized emails, supports file attachments and inline images, and sends emails securely using the SMTP protocol. It also supports scheduled email delivery based on the time specified in the CSV file.

---

## Features

- Automatic email sending
- Multiple recipient support
- CSV-based recipient management
- File attachment support
- Inline image support
- SMTP authentication
- Email scheduling

---

## Project Structure

```text
Automated_Email_Sender/
│
├── Automated_email_sender.py
├── recipients.csv
├── README.md
│
├── attachment/
│   └── report.pdf
│
└── images/
    └── images.jpeg
```

---

## Requirements

- Python 3.9 or above

Install the required package:

```bash
pip install schedule
```

---

### Attachment Folder

```
attachment/
```

Place the file that you want to attach inside this folder and add that file name in the code.

Example:

```
attachment/report.pdf
```

### Images Folder

```
images/
```

Place the image that you want to display inside the email and that image name in the code.

Example:

```
images/images.jpeg
```

---

## SMTP Configuration

Open `Automated_email_sender.py`.

Inside the `ConfigLoader` class, replace the following values with your own Gmail address and Google App Password.

```python
self.sender_email = "your_email@gmail.com"
self.sender_password = "your_google_app_password"
```

For Gmail users:

1. Enable Two-Step Verification.
2. Generate a Google App Password.
3. Replace the sender email and App Password with your own credentials.

SMTP Configuration:

```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

---

## CSV Format

The `recipients.csv` file should contain the following columns:

| name | email | attachment | image | schedule |
|------|-------|------------|--------|----------|

Example:

```csv
name,email,attachment,image,schedule
John,john@gmail.com,attachment/report.pdf,images/images.jpeg,10:00
Alice,alice@gmail.com,attachment/report.pdf,images/images.jpeg,10:30
```

### Column Description

| Column | Description |
|---------|-------------|
| name | Recipient name |
| email | Recipient email address |
| attachment | File attachment path |
| image | Inline image path |
| schedule | Time to send email (HH:MM) |

---

The program currently uses:

```python
run_email_batch(CSV_PATH, SUBJECT, BODY)
```

This sends emails immediately to all recipients.

---

## Scheduled Email

If you want to send emails automatically according to the time specified in the **schedule** column of `recipients.csv`, replace:

```python
run_email_batch(CSV_PATH, SUBJECT, BODY)
```

with

```python
start_scheduler(CSV_PATH, SUBJECT, BODY)
```

The scheduler continuously checks the current system time. When the current time matches the value in the **schedule** column, the email is sent automatically.

Example:

```csv
name,email,schedule
John,john@gmail.com,14:30
Alice,alice@gmail.com,15:00
```

John's email will be sent at **14:30** and Alice's email will be sent at **15:00**.

---

## Workflow

```text
Start
   │
   ▼
Read recipients.csv
   │
   ▼
Load Recipient Details
   │
   ▼
Compose Email
   │
   ▼
Attach Files
   │
   ▼
Attach Inline Image
   │
   ▼
Connect to SMTP Server
   │
   ▼
Authenticate Sender
   │
   ▼
Send Email
   │
   ▼
Next Recipient
   │
   ▼
End
```

---

## Technologies Used

- Python
- SMTP
- CSV
- MIME
- TLS Encryption
- Schedule Library

---

## Author

Ayushya Lakshmi Nagireddy

---

## License

This project is developed for educational and learning purposes.
