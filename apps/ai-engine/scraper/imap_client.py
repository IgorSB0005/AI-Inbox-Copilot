import socket
from imap_tools import MailBox, A
from typing import List, Dict, Any

class GmailScraper:
    def __init__(self, email: str, app_password: str):
        self.email = email
        self.app_password = app_password
        self.imap_server = "imap.gmail.com"

    def fetch_unread_emails(self) -> List[Dict[str, Any]]:
        """
        Connects to imap.gmail.com, fetches all UNSEEN emails, extracts
        subject, sender, and raw body, and marks them as SEEN.
        Handles timeouts gracefully.
        """
        emails = []
        try:
            # Use a timeout for network resilience
            with MailBox(self.imap_server, timeout=15).login(self.email, self.app_password) as mailbox:
                # fetch defaults to mark_seen=True, so it marks fetched emails as SEEN
                for msg in mailbox.fetch(A(seen=False), mark_seen=True):
                    emails.append({
                        "subject": msg.subject,
                        "sender": msg.from_,
                        "raw_body": msg.html or msg.text or ""
                    })
        except socket.timeout:
            print(f"Timeout error while trying to connect to {self.imap_server}")
        except Exception as e:
            print(f"An error occurred while fetching emails: {e}")
            
        return emails
