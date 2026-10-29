import sqlite3
from langchain_community.chat_message_histories import SQLChatMessageHistory
from src.config import DB_URI, RAW_DB_PATH

def init_db():
    """Initializes the SQLite tables for entity memory and ticketing."""
    conn = sqlite3.connect(RAW_DB_PATH)
    cursor = conn.cursor()

    # 1. User Accounts Table (Entity Memory)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_accounts (
            email TEXT PRIMARY KEY,
            tier TEXT NOT NULL
        )
    """)

    # 2. Support Tickets Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS support_tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            category TEXT NOT NULL,
            severity TEXT NOT NULL,
            summary TEXT NOT NULL,
            status TEXT DEFAULT 'OPEN',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 3. Inject mock data for testing
    cursor.execute("SELECT COUNT(*) FROM user_accounts")
    if cursor.fetchone()[0] == 0:
        mock_users = [
            ("vip@example.com", "VIP"),
            ("standard@example.com", "Standard")
        ]
        cursor.executemany("INSERT INTO user_accounts (email, tier) VALUES (?, ?)", mock_users)
        
    conn.commit()
    conn.close()

def get_chat_history(session_id: str) -> SQLChatMessageHistory:
    """
    LangChain's built-in SQLite history manager.
    Automatically handles the message_store table creation and schema.
    """
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string=DB_URI
    )

def fetch_user_tier(email: str) -> str:
    """
    Utility function used to retrieve the user's tier for system prompt injection.
    """
    conn = sqlite3.connect(RAW_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT tier FROM user_accounts WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else "Unknown"

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {RAW_DB_PATH}")