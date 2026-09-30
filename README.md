# 📧 Smart Email Analyzer — AI Executive Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-3.5%20Flash%20Lite-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Model Context Protocol](https://img.shields.io/badge/Protocol-MCP-4B32C3?style=for-the-badge)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Smart Email Analyzer** is an AI-powered Django web application that acts as an intelligent executive email assistant. By directly integrating with the **Google Gmail API** and powered by **Google Gemini AI** via **Model Context Protocol (MCP)** tools, it enables users to search, summarize, analyze, and query their email inbox and document attachments using natural language.

---

## 📋 Table of Contents

1. [🌟 Project Overview & Key Features](#-project-overview--key-features)
2. [🛠 Technical Stack](#-technical-stack)
3. [📂 Project Structure](#-project-structure)
4. [🔐 Authentication & Security (OAuth 2.0 PKCE)](#-authentication--security-oauth-20-pkce)
5. [📄 Gmail Engine & Multi-Format Parsing](#-gmail-engine--multi-format-parsing)
6. [🤖 Model Context Protocol (MCP) Infrastructure](#-model-context-protocol-mcp-infrastructure)
7. [🧠 AI Agent & Google Gemini Integration](#-ai-agent--google-gemini-integration)
8. [🔄 Dual-Mode Operations](#-dual-mode-operations)
9. [🎨 Frontend Architecture & Design System](#-frontend-architecture--design-system)
10. [⚙️ Installation & Local Setup](#-installation--local-setup)
11. [🔒 Privacy & Security Policies](#-privacy--security-policies)

---

## 🌟 Project Overview & Key Features

* **Natural Language Inbox Querying**: Ask questions like *"Did I receive any interview emails?"*, *"Summarize recent messages from HR"*, or *"Find emails with PDF invoices"* without memorizing search syntax.
* **Strictly Read-Only Security**: Interacts with Gmail exclusively through `gmail.readonly` scopes, ensuring zero write, delete, or unintended email modification operations.
* **Multi-Format Attachment Parsing**: Deeply inspects email attachments on demand, extracting text and tables from **PDF** (`.pdf`), **Word** (`.docx`, `.doc`), **Excel** (`.xlsx`, `.xls`), and **CSV** (`.csv`) files.
* **Model Context Protocol (MCP) Tools**: Exposes 20+ specialized read-only tool functions to Gemini AI, enabling real-time autonomous tool calling for email searches, counting, sender filtering, and content extraction.
* **Dual-Mode System**:
  * **Gmail Inbox Mode**: Queries live Gmail inbox messages, threads, and attachments in real time.
  * **Document Analysis Mode**: Inspects user-uploaded documents (`.pdf`, `.docx`, `.xlsx`, `.csv`, `.txt`) using document-level MCP tools.
* **Modern SPA Interface**: Built with a sleek Glassmorphism UI, HSL color tokens, an anti-flicker light/dark mode switcher, live typing indicators, and a responsive layout.

---

## 🛠 Technical Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend Framework** | Python 3.10+ / Django 6.0 | MVT Architecture, Session Management, CSRF Security |
| **AI Model & SDK** | `google-genai` SDK | Gemini 3.5 Flash Lite with Automatic Function Calling (AFC) |
| **Tool Protocol** | Model Context Protocol (MCP) | 20+ Gmail tools and 6 Document analysis tools |
| **External APIs** | Google Gmail API v1, OAuth 2.0 | Read-only inbox retrieval with PKCE verification |
| **Attachment Parsing** | `PyPDF2`, `python-docx`, `pandas`, `openpyxl` | In-memory text extraction for PDF, DOCX, XLSX, and CSV |
| **Database** | SQLite3 | Stores custom User model and refreshed OAuth credentials |
| **Frontend** | HTML5, CSS3, JavaScript (ES6 AJAX) | Custom Glassmorphism design, FontAwesome 6, Google Fonts |

---

## 📂 Project Structure

```text
smart-email-analyzer/
├── manage.py                # Django CLI management entry point
├── requirements.txt         # Project Python dependencies
├── .env.example             # Template for required environment variables
├── .gitignore               # Excludes secrets, venv, sqlite, and caches
├── README.md                # Project documentation
├── PROJECT_PITCH.md         # Initial project pitch & feature overview
├── config/                  # Django project root configuration
│   ├── settings.py          # Application settings & environment configuration
│   ├── urls.py              # Root URL routing table
│   ├── asgi.py              # ASGI configuration
│   └── wsgi.py              # WSGI configuration
├── accounts/                # Authentication & User Management
│   ├── models.py            # Custom User model storing OAuth tokens
│   ├── views.py             # Google OAuth 2.0 PKCE login, callback & logout
│   └── urls.py              # Authentication endpoints (/accounts/login, /accounts/google, etc.)
├── gmail/                   # Gmail API Data Engine
│   ├── services.py          # API fetching & MIME attachment text extraction (PDF/Docx/Excel)
│   ├── views.py             # Inbox view handlers
│   └── urls.py              # Gmail routes (/gmail/inbox/)
├── mcp/                     # Model Context Protocol Tools Layer
│   ├── tools.py             # MCPTools class defining 20+ Gmail search & read tools
│   ├── gmail_service.py     # GmailClient credentials & token auto-refresh manager
│   └── document_tools.py    # DocumentMCPTools for local uploaded file queries
├── ai/                      # AI Engine & Gemini Integration
│   └── services.py          # Gemini client setup, function calling loop, system prompts
├── chat/                    # Chat Web Application (SPA)
│   ├── views.py             # Chat endpoints (/api/send_message/, /api/upload_document/)
│   └── urls.py              # Chat routes
├── templates/               # HTML Templates
│   ├── base.html            # Master layout, header, anti-flicker theme script, footer
│   ├── accounts/
│   │   └── login.html       # Google OAuth login landing page
│   └── chat/
│       ├── chat.html        # SPA Chat interface and input form
│       └── dashboard.html   # Assistant overview dashboard
└── static/                  # Static Web Assets
    ├── css/
    │   └── style.css        # HSL Glassmorphism design system & Light/Dark mode CSS
    └── js/
        └── app.js           # AJAX message dispatcher, theme toggle, document badge handler
```

---

## 🔐 Authentication & Security (OAuth 2.0 PKCE)

1. **Custom User Model** (`accounts/models.py`):
   Extends `AbstractUser` to securely persist:
   * `google_access_token`: Short-lived token for Gmail API access.
   * `google_refresh_token`: Long-lived token used to acquire new access tokens.
   * `google_token_expiry`: Expiration timestamp in UTC.

2. **PKCE Verification Flow** (`accounts/views.py`):
   * Generates a code verifier and code challenge using RFC 7636 PKCE standards.
   * Scopes requested:
     * `https://www.googleapis.com/auth/gmail.readonly`
     * `https://www.googleapis.com/auth/userinfo.email`
     * `https://www.googleapis.com/auth/userinfo.profile`
     * `openid`

3. **Silent Token Refresh** (`mcp/gmail_service.py`):
   * When an access token expires, the credentials manager invokes `Credentials.refresh(Request())` to refresh tokens seamlessly without requiring user re-authentication.

---

## 📄 Gmail Engine & Multi-Format Parsing

The ingestion pipeline in `gmail/services.py` recursively parses email payloads:

* **PDF Documents (`.pdf`)**: Downloaded via the Gmail attachments API, decoded from base64 in memory, and parsed page-by-page using `PyPDF2.PdfReader`.
* **Word Documents (`.docx`, `.doc`)**: Read in memory and converted using `python-docx.Document`, capturing formatted paragraphs.
* **Spreadsheets (`.xlsx`, `.xls`, `.csv`)**: Loaded into `pandas.DataFrame` objects and converted into tabular strings (`df.to_string()`).
* Extracted attachment contents are automatically injected into the tool result payload under clearly labeled delimiters:
  ```text
  --- Attachment: report.pdf ---
  [Extracted content...]
  --- End of Attachment ---
  ```

---

## 🤖 Model Context Protocol (MCP) Infrastructure

The system employs standard Model Context Protocol (MCP) tool declarations in `mcp/tools.py`:

```python
class MCPTools:
    def search_emails(self, keyword: str) -> list: ...
    def read_email(self, email_id: str) -> dict: ...
    def get_today_emails(self) -> list: ...
    def get_recent_emails(self, max_results: int = 10) -> list: ...
    def get_sent_emails(self, max_results: int = 10) -> list: ...
    def get_unread_emails(self) -> list: ...
    def get_interview_emails(self) -> list: ...
    def get_hr_emails(self) -> list: ...
    def search_sender(self, sender_name: str) -> list: ...
    def search_subject(self, keyword: str) -> list: ...
    def search_date(self, date: str) -> list: ...
    def get_attachment_emails(self) -> list: ...
    def get_pdf_emails(self) -> list: ...
    def get_docx_emails(self) -> list: ...
    def get_excel_emails(self) -> list: ...
    def get_meeting_emails(self) -> list: ...
    def get_important_emails(self) -> list: ...
    def get_security_emails(self) -> list: ...
    def count_today(self) -> dict: ...
    def count_total(self) -> dict: ...
    def count_unread(self) -> dict: ...
    def count_interview(self) -> dict: ...
    def count_security(self) -> dict: ...
```

* **Tool Discovery**: `mcp.get_all_tools()` passes the bound methods directly into `GenerateContentConfig(tools=mcp.get_all_tools())`.
* **Automatic Function Calling**: Configured through `types.AutomaticFunctionCallingConfig(disable=False)`, allowing Gemini to chain searches and detail lookups autonomously.

---

## 🧠 AI Agent & Google Gemini Integration

In `ai/services.py`, the assistant runs on **Google Gemini 3.5 Flash Lite** with strictly engineered system prompts and guardrails:

* **Strict Domain Boundary**: Gemini is instructed to solely answer queries related to the user's emails or uploaded files. Any non-domain query returns a polite refusal.
* **Anti-Hallucination Search-to-Read Pipeline**: Search tools return high-level snippets; the model is instructed to call `read_email` to inspect full contents before stating conclusions.
* **Third-Party Clarification**: Distinguishes direct company communication from third-party aggregators (e.g. LinkedIn digests or job board alerts).
* **Plain Text Output**: Strips raw markdown backticks and asterisks to maintain clean rendering in the chat interface.

---

## 🔄 Dual-Mode Operations

1. **Gmail Inbox Mode (Default)**:
   * Queries real-time Gmail inbox using `MCPTools`.
   * Answers questions regarding threads, unread emails, sender history, and email attachments.
2. **Uploaded Document Analysis Mode**:
   * Activated dynamically when a user uploads a file through the chat interface.
   * Seamlessly switches to `DocumentMCPTools` and specialized document analysis instructions.
   * Supports local analysis of `.pdf`, `.docx`, `.xlsx`, `.csv`, and `.txt` files.

---

## 🎨 Frontend Architecture & Design System

* **Glassmorphism Design System** (`static/css/style.css`): Modern, translucent cards with subtle borders and shadows using curated HSL color palettes.
* **Anti-Flicker Theme Engine** (`templates/base.html`): Inline synchronous head script detects theme preference (`localStorage` or `prefers-color-scheme`) prior to DOM rendering, preventing theme flickering.
* **Responsive SPA UX** (`static/js/app.js`):
  * Dynamic AJAX message stream with animated typing indicator.
  * Instant New Chat session reset.
  * Drag-and-drop document upload with active attachment badge.

---

## ⚙️ Installation & Local Setup

### 1. Prerequisites
* **Python 3.10+** (Tested on Python 3.13)
* **Google Cloud Console Project** with:
  * **Gmail API** enabled
  * OAuth 2.0 Credentials configured with authorized redirect URI: `http://127.0.0.1:8000/accounts/google/callback/`
* **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com/)

### 2. Clone the Repository
```bash
git clone https://github.com/Mithun1075/smart-email-analyzer.git
cd smart-email-analyzer
```

### 3. Set Up Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy the `.env.example` template to `.env`:
```bash
cp .env.example .env
```

Open `.env` and fill in your actual credentials:
```env
# Django Settings
SECRET_KEY=your_secure_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Google OAuth Credentials
GOOGLE_OAUTH_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URL=http://127.0.0.1:8000/accounts/google/callback/

# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key
```

### 6. Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser, log in with your Gmail account, and start chatting with your AI executive assistant!

---

## 🔒 Privacy & Security Policies

* **Read-Only Access**: The application exclusively requests read permissions (`gmail.readonly`). It cannot send, forward, delete, or modify any emails.
* **Ephemeral In-Memory Parsing**: Email bodies and attachments are extracted on-the-fly and are never permanently stored on disk.
* **Protected Secrets**: Sensitive secrets and database files are protected through `.gitignore` and `.env` configuration.
