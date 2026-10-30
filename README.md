# 🤖 Autonomous AI Service Desk

An intelligent, tool-calling AI support desk that autonomously resolves enterprise IT tickets, enforces company policies via Retrieval-Augmented Generation (RAG), and executes third-party integrations based on SQL-driven user permission tiers.

Built with **LangChain**, **Groq**, **ChromaDB**, and **Streamlit**, this system acts as a Level-0 support engineer, completely automating repetitive IT requests, reducing ticket bloat, and providing white-glove service to VIP users.

---

## ✨ Core Capabilities

* **Secure Authentication & State:** Streamlit modal authentication with session-state memory tracking across the conversation.
* **Tier-Based Dynamic Logic (SQLite):** Queries a local SQL database to determine if a user is `Standard` or `VIP`, dynamically altering its workflow.
* **Retrieval-Augmented Generation (ChromaDB):** Ingests Markdown policy files to accurately enforce company rules regarding hardware damage and software refunds.
* **Intelligent Tool Execution:** Natively utilizes the `gpt-oss-120b` model to decide when to trigger specific Python functions:
* `query_company_policy`: Fetches RAG context.
* `fetch_account_details`: Looks up SQL database rows.
* `check_system_status`: Deflects tickets for known global outages.
* `create_support_ticket`: Writes new tickets to the database.
* `send_email_confirmation`: Connects to Gmail SMTP to dispatch real-time alerts.
* `check_and_book_calendar`: Interfaces with Google Calendar to schedule mediation meetings.


* **Synchronous UI Streaming:** Bypasses asynchronous LangChain callback crashes by executing natively on the main thread, resulting in a perfectly stable, enterprise-grade loading UI.

---

## 🏗️ Architecture & Tech Stack

* **Frontend Interface:** [Streamlit](https://streamlit.io/) (`1.33.0`)
* **Cognitive Framework:** [LangChain](https://www.langchain.com/) (`0.1.16`)
* **LLM Inference Engine:** [Groq](https://groq.com/) (`openai/gpt-oss-120b`) via `langchain-groq` (`0.1.3`)
* **Vector Database (RAG):** [ChromaDB](https://www.trychroma.com/) (`0.4.24`)
* **Embeddings:** `sentence-transformers`
* **Relational Database:** SQLite3
* **Integrations:** Gmail SMTP, Google Calendar API

---

## 🚀 Local Installation & Setup

### 1. Prerequisites

* **Python 3.12+**
* **C++ Compiler:** If you are on Windows, you must install [Microsoft Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and check the **"Desktop development with C++"** workload. This is strictly required to compile the `chroma-hnswlib` dependency.

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/service-desk.git
cd service-desk

```

### 3. Set Up the Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the root directory and add the following keys. **Do not commit this file to version control.**

```text
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=openai/gpt-oss-120b

# Gmail SMTP Configuration for sending ticket alerts
SENDER_EMAIL=your_email@gmail.com
SENDER_APP_PASSWORD=your_16_digit_app_password
```

### 5. Add API Credentials

If you are utilizing the Google Calendar tool, place your Google Cloud OAuth credentials file in the root directory:

* `credentials.json`
*(Note: A `token.json` will be auto-generated upon your first successful login).*

---

## 🕹️ Running the Application

1. **Launch the Streamlit Server:**

```bash
streamlit run src/app.py
```

2. **Access the UI:** Open `http://localhost:8501` in your browser.
3. **Authenticate:** Use the modal to log in. Try testing different persona tiers:
* `standard@example.com`
* `vip@example.com`



---

## 🧪 Recommended Test Scenarios

To see the agent dynamically route logic, try these prompts after logging in as different users:

**Test 1: The Policy Enforcer (Login as `standard@example.com`)**

> *"I spilled coffee on my laptop. I need a replacement ordered immediately."*

* **Result:** The agent checks the DB, reads the standard RAG policy, and politely refuses to order the hardware without photographic evidence.

**Test 2: The VIP White-Glove Override (Login as `vip@example.com`)**

> *"My laptop screen is shattered. Log a ticket and email me confirmation."*

* **Result:** The agent identifies the VIP tier, creates a High-Severity SQL ticket, and dispatches the SMTP email.

**Test 3: The Outage Deflection (Any User)**

> *"The billing system is completely down and keeps giving me a 500 error."*

* **Result:** The agent checks the system status tool, sees the active global outage, and explains the situation to the user without duplicating existing IT tickets.