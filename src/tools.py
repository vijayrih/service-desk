import os
import sqlite3
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

from langchain_core.tools import tool
from src.config import RAW_DB_PATH, SENDER_EMAIL, SENDER_APP_PASSWORD

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Internal Data Tools

@tool
def fetch_account_details(email: str) -> str:
    """
    Fetches the user's account tier (VIP or Standard) from the database.
    Use this to determine if the user gets priority routing or VIP SLAs.
    """
    conn = sqlite3.connect(RAW_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT tier FROM user_accounts WHERE email = ?", (email,))
    res = cursor.fetchone()
    conn.close()
    
    if res:
        return f"Account found. Tier: {res[0]}"
    return "Account not found in the system."

@tool
def check_system_status(service_name: str) -> str:
    """
    Checks if an internal system (e.g., 'main_app', 'authentication', 'billing') 
    is currently experiencing a global outage. Use this to deflect tickets if a system is down.
    """

    outages = {
        "authentication": "Operational",
        "billing": "Degraded Performance",
        "main_app": "Operational"
    }
    service = service_name.lower()
    status = outages.get(service, "Operational")
    return f"Status for {service}: {status}"

# Ticketing Tool

@tool
def create_support_ticket(email: str, category: str, severity: str, summary: str) -> str:
    """
    Logs a support ticket into the internal tracking system. 
    Use this for hardware issues, unresolved software crashes, or escalations.
    Categories: Hardware, Software, Billing, Other.
    Severities: Low, Medium, High.
    """
    try:
        conn = sqlite3.connect(RAW_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO support_tickets (email, category, severity, summary) VALUES (?, ?, ?, ?)", 
            (email, category, severity, summary)
        )
        ticket_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return f"Ticket successfully created. Ticket ID: TKT-{ticket_id}"
    except Exception as e:
        return f"Failed to create ticket: {str(e)}"

# Email Dispatcher

@tool
def send_email_confirmation(to_email: str, subject: str, body: str) -> str:
    """
    Sends an official email to the customer. 
    Use this to send ticket IDs, resolutions, or calendar meeting links.
    """
    if not SENDER_EMAIL or not SENDER_APP_PASSWORD:
        return "System Error: Email credentials not configured on the server."
    
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return f"Email successfully dispatched to {to_email}."
    except Exception as e:
        return f"Failed to send email: {str(e)}"

# Google Calendar Integration

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def _get_calendar_service():
    """Authenticates with Google Calendar using OAuth 2.0."""
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError("credentials.json is missing! Download it from GCP.")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return build('calendar', 'v3', credentials=creds)

@tool
def check_and_book_calendar(date_str: str, time_str: str, duration_minutes: int, attendee_email: str) -> str:
    """
    Books a Google Calendar meeting with a human support manager.
    date_str MUST be in format: YYYY-MM-DD
    time_str MUST be in format: HH:MM (24-hour format)
    """
    try:
        service = _get_calendar_service()
        
        start_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        
        event = {
          'summary': 'Tier-1 Support Escalation',
          'description': f'Escalation meeting with {attendee_email}.',
          'start': {
              'dateTime': start_dt.isoformat(),
              'timeZone': 'UTC',
          },
          'end': {
              'dateTime': end_dt.isoformat(),
              'timeZone': 'UTC',
          },
          'attendees': [
              {'email': attendee_email}
          ],
        }
        
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return f"Meeting booked successfully! Event Link: {event_result.get('htmlLink')}"
    
    except Exception as e:
        return f"Failed to book calendar. Error: {str(e)}"

if __name__ == "__main__":
    print("Testing tools and generating token.json for Google Calendar...")
    try:
        _get_calendar_service()
        print("Google Calendar Auth Successful! token.json created.")
        
        print("\nTesting DB Check...")
        print(fetch_account_details.invoke({"email": "vip@example.com"}))
    except Exception as e:
        print(f"Error: {e}")