"""Send formatted emails via Gmail SMTP."""
import smtplib
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender:
    """Sends emails via Gmail SMTP."""

    def __init__(self, gmail_user: str, gmail_password: str):
        self.gmail_user = gmail_user
        self.gmail_password = gmail_password
        self.max_retries = 3

    def _send_email(self, recipient: str, subject: str, plain_text: str, html_content: str = "") -> bool:
        """Send an email with retries for transient SMTP failures."""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.gmail_user
        msg['To'] = recipient

        msg.attach(MIMEText(plain_text, 'plain'))
        if html_content:
            msg.attach(MIMEText(html_content, 'html'))

        for attempt in range(1, self.max_retries + 1):
            try:
                print("Connecting to Gmail SMTP server...")
                with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as server:
                    server.starttls()
                    print("Logging in...")
                    server.login(self.gmail_user, self.gmail_password)
                    print(f"Sending email to {recipient}...")
                    server.send_message(msg)
                print("Email sent successfully!")
                return True
            except smtplib.SMTPAuthenticationError:
                print("ERROR: Gmail authentication failed.")
                print("Make sure you're using an App Password, not your regular Gmail password.")
                print("Visit: https://myaccount.google.com/apppasswords")
                return False
            except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError, TimeoutError) as e:
                if attempt == self.max_retries:
                    print(f"ERROR: Failed to send email after {self.max_retries} attempts: {e}")
                    return False
                wait_seconds = 2 ** attempt
                print(f"SMTP transient error (attempt {attempt}/{self.max_retries}): {e}. Retrying in {wait_seconds}s...")
                time.sleep(wait_seconds)
            except Exception as e:
                print(f"ERROR: Failed to send email: {e}")
                return False

    def send_digest(self, recipient: str, html_content: str, plain_text: str, subject: str = "") -> bool:
        """Send the news digest email."""
        today = datetime.now().strftime("%B %d, %Y")
        if not subject:
            subject = f"The Brief \u2014 {today}"

        return self._send_email(recipient, subject, plain_text, html_content)

    def send_failure_alert(self, recipient: str, error_message: str) -> bool:
        """Send a plain-text failure alert when digest generation fails."""
        today = datetime.now().strftime("%B %d, %Y")
        subject = f"NewsAgent Failed Run Alert - {today}"
        body = (
            "Your NewsAgent run failed.\n\n"
            f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Error: {error_message}\n\n"
            "Check logs and retry once the issue is resolved."
        )
        return self._send_email(recipient, subject, body)
