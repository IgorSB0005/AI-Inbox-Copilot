import socket
from imap_tools import MailBox, A
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

class GmailScraper:
    def __init__(self, email: str, app_password: str):
        self.email = email
        self.app_password = app_password
        self.imap_server = "imap.gmail.com"

    def fetch_unread_emails(self, start_datetime: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Connects to imap.gmail.com, fetches all UNSEEN emails, extracts
        subject, sender, and raw body, and marks them as SEEN.
        If start_datetime is provided, strictly ignores emails older than that time.
        Handles timeouts gracefully.
        """
        emails = []
        try:
            # Use a timeout for network resilience
            with MailBox(self.imap_server, timeout=15).login(self.email, self.app_password) as mailbox:
                
                # If we have a datetime, filter IMAP by date to drastically reduce payload
                search_criteria = A(seen=False)
                if start_datetime:
                    search_criteria = A(seen=False, date_gte=start_datetime.date())
                
                # fetch defaults to mark_seen=True, so it marks fetched emails as SEEN
                for msg in mailbox.fetch(search_criteria, mark_seen=True):
                    
                    # IMAP date_gte only filters by day. Enforce strict time-level filtering here.
                    if start_datetime:
                        # Ensure timezone awareness matches for comparison
                        msg_date = msg.date if msg.date.tzinfo else msg.date.replace(tzinfo=timezone.utc)
                        start_dt = start_datetime if start_datetime.tzinfo else start_datetime.replace(tzinfo=timezone.utc)
                        
                        if msg_date < start_dt:
                            continue

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
