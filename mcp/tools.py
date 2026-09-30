from datetime import datetime
from gmail.services import search_gmail, count_gmail, get_email_details

class MCPTools:
    """
    Model Context Protocol (MCP) compatible tools for Gmail.
    Provides a strictly read-only interface to the AI.
    """
    def __init__(self, user):
        self.user = user

    def search_emails(self, keyword: str) -> list:
        """Search emails using a general keyword."""
        return search_gmail(self.user, query=keyword)

    def read_email(self, email_id: str) -> dict:
        """Read the full details of a specific email by its ID."""
        return get_email_details(self.user, email_id)

    def get_today_emails(self) -> list:
        """Get emails received today (since midnight)."""
        today_str = datetime.now().strftime('%Y/%m/%d')
        return search_gmail(self.user, query=f"after:{today_str}")

    def get_unread_emails(self) -> list:
        """Get unread emails."""
        return search_gmail(self.user, query="is:unread")

    def get_interview_emails(self) -> list:
        """Get emails related to job interviews."""
        return search_gmail(self.user, query="interview OR schedule OR assessment")

    def get_hr_emails(self) -> list:
        """Get emails from HR or recruiting."""
        return search_gmail(self.user, query="hr OR human resources OR recruiter OR talent")

    def search_sender(self, sender_name: str) -> list:
        """Search emails by a specific sender name or email address. Returns only snippets. Use read_email for full content."""
        return search_gmail(self.user, query=f"from:{sender_name}")

    def search_subject(self, keyword: str) -> list:
        """Search emails where the subject contains a specific keyword."""
        return search_gmail(self.user, query=f"subject:{keyword}")

    def search_date(self, date: str) -> list:
        """Search emails received on or after a specific date (YYYY/MM/DD)."""
        return search_gmail(self.user, query=f"after:{date}")

    def get_attachment_emails(self) -> list:
        """Get emails that contain any attachments."""
        return search_gmail(self.user, query="has:attachment")

    def get_pdf_emails(self) -> list:
        """Get emails that contain PDF attachments."""
        return search_gmail(self.user, query="filename:pdf")

    def get_docx_emails(self) -> list:
        """Get emails that contain Word document (DOCX/DOC) attachments."""
        return search_gmail(self.user, query="filename:docx OR filename:doc")

    def get_excel_emails(self) -> list:
        """Get emails that contain Excel (XLSX/XLS) attachments."""
        return search_gmail(self.user, query="filename:xlsx OR filename:xls")

    def get_latest_email(self) -> list:
        """Get the single most recent email in the inbox."""
        return search_gmail(self.user, query="in:inbox", max_results=1)

    def get_recent_emails(self, max_results: int = 10) -> list:
        """Get the most recent emails received in the INBOX (query='in:inbox')."""
        return search_gmail(self.user, query="in:inbox", max_results=max_results)

    def get_sent_emails(self, max_results: int = 10) -> list:
        """Get emails sent by the authenticated user (query='from:me OR in:sent')."""
        return search_gmail(self.user, query="from:me OR in:sent", max_results=max_results)

    def count_today(self) -> dict:
        """Get the total count of emails received today (since midnight)."""
        today_str = datetime.now().strftime('%Y/%m/%d')
        return count_gmail(self.user, query=f"after:{today_str}")

    def count_total(self) -> dict:
        """Get the total count of all emails in the inbox."""
        return count_gmail(self.user, query="")

    def count_search(self, keyword: str) -> dict:
        """Get the total count of emails matching a specific search keyword."""
        return count_gmail(self.user, query=keyword)

    def count_unread(self) -> dict:
        """Get the total count of unread emails."""
        return count_gmail(self.user, query="is:unread")

    def count_interview(self) -> dict:
        """Get the total count of interview-related emails."""
        return count_gmail(self.user, query="interview OR schedule OR assessment")

    def get_meeting_emails(self) -> list:
        """Get emails containing meeting invitations or calendar links."""
        return search_gmail(self.user, query="invite OR meeting OR calendar OR zoom OR meet")

    def get_important_emails(self) -> list:
        """Get emails marked as important or urgent."""
        return search_gmail(self.user, query="is:important OR urgent OR action required")

    def get_security_emails(self) -> list:
        """Get security alerts and account notification emails."""
        return search_gmail(self.user, query="security OR alert OR warning OR password OR login OR unauthorized")

    def count_security(self) -> dict:
        """Get the total count of security-related emails."""
        return count_gmail(self.user, query="security OR alert OR warning OR password OR login OR unauthorized")

    def get_all_tools(self):
        """Returns a list of all bound methods to be passed to Gemini."""
        return [
            self.search_emails,
            self.read_email,
            self.get_today_emails,
            self.get_recent_emails,
            self.get_sent_emails,
            self.get_unread_emails,
            self.get_interview_emails,
            self.get_hr_emails,
            self.search_sender,
            self.search_subject,
            self.search_date,
            self.get_attachment_emails,
            self.get_pdf_emails,
            self.get_docx_emails,
            self.get_excel_emails,
            self.get_latest_email,
            self.count_today,
            self.count_total,
            self.count_search,
            self.count_unread,
            self.count_interview,
            self.get_meeting_emails,
            self.get_important_emails,
            self.get_security_emails,
            self.count_security
        ]
