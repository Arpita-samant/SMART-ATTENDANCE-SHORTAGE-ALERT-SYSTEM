#!/usr/bin/env python3
import os
import sys
import io
import csv
import json
import smtplib
import email.mime.multipart
import email.mime.text

# ── Change these ──────────────────────────────────────
SENDER_EMAIL    = "samantarpita70@gmail.com"
SENDER_PASSWORD = "ltcu fggl laev zmyo"
# ─────────────────────────────────────────────────────

ATTENDANCE_THRESHOLD = 75


def parse_multipart():
    """Manually parse multipart/form-data to extract the uploaded CSV."""
    
    content_type = os.environ.get("CONTENT_TYPE", "")
    content_length = int(os.environ.get("CONTENT_LENGTH", 0))

    raw_body = sys.stdin.buffer.read(content_length)

    # Extract boundary from Content-Type header
    boundary = None

    for part in content_type.split(";"):
        part = part.strip()

        if part.startswith("boundary="):
            boundary = part[len("boundary="):].strip()
            break

    if not boundary:
        return None

    boundary_bytes = ("--" + boundary).encode()
    parts = raw_body.split(boundary_bytes)

    for part in parts:

        # Find uploaded csv_file
        if b'name="csv_file"' in part:

            # Split headers and body
            if b"\r\n\r\n" in part:
                _, file_data = part.split(b"\r\n\r\n", 1)

                # Remove extra ending characters
                file_data = file_data.rstrip(b"\r\n--")

                return file_data.decode("utf-8")

    return None


def send_email(student_name, student_email, percentage):

    subject = "⚠️ Low Attendance Alert"

    body = f"""Dear {student_name},

This is an automated alert from your institution.

Your current attendance is {percentage:.1f}%, which is below the required 75%.

Please attend classes regularly to avoid any academic penalty.

Regards,
Smart Attendance Alert System
"""

    msg = email.mime.multipart.MIMEMultipart()

    msg["From"] = SENDER_EMAIL
    msg["To"] = student_email
    msg["Subject"] = subject

    msg.attach(email.mime.text.MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        server.sendmail(
            SENDER_EMAIL,
            [student_email],
            msg.as_string()
        )


def main():

    print("Content-Type: application/json")
    print()

    file_data = parse_multipart()

    if not file_data:
        print(json.dumps({
            "error": "No file uploaded or could not parse file."
        }))
        return

    students = []
    alerts_sent = 0
    errors = []

    # Count number of emails sent
    email_count = {}

    try:

        reader = csv.DictReader(io.StringIO(file_data))

        for row in reader:

            # Remove extra spaces
            row = {k.strip(): v.strip() for k, v in row.items()}

            name = row.get("Name", "")
            email_id = row.get("Email", "")

            attended = int(row.get("Attended", "0"))
            total = int(row.get("Total", "1"))

            # ── Validation Checks ─────────────────────

            if attended < 0 or total < 0:
                errors.append(
                    f"Invalid negative values for {name}"
                )
                continue

            if attended > total:
                errors.append(
                    f"Attendance error for {name}: "
                    f"Attended classes cannot be greater than total classes."
                )
                continue

            if total == 0:
                percentage = 0
            else:
                percentage = (attended / total) * 100

            students.append({
                "name": name,
                "email": email_id,
                "attended": attended,
                "total": total,
                "percentage": round(percentage, 2)
            })

            # ── Send Alert if Attendance is Low ──────

            if percentage < ATTENDANCE_THRESHOLD:

                try:
                    send_email(name, email_id, percentage)

                    alerts_sent += 1

                    # Count emails sent to each student
                    if email_id in email_count:
                        email_count[email_id] += 1
                    else:
                        email_count[email_id] = 1

                except Exception as e:
                    errors.append(
                        f"Failed to email {name}: {str(e)}"
                    )

    except Exception as e:

        print(json.dumps({
            "error": f"CSV parsing error: {str(e)}"
        }))

        return

    # ── Final Output ────────────────────────────────

    print(json.dumps({
        "total_students": len(students),
        "alerts_sent": alerts_sent,
        "email_count": email_count,
        "students": students,
        "errors": errors
    }, indent=4))


main()