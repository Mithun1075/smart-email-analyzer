# Smart Mail Analyzer - Project Overview & Team Pitch

## 1. What is "Smart Mail Analyzer"?
**Smart Mail Analyzer** is an AI-powered web application designed to help users intelligently manage, search, and analyze their email inboxes. It integrates directly with a user's Gmail account and leverages state-of-the-art Generative AI (like Google's Gemini models) to act as an advanced email assistant.

Instead of just presenting a list of emails, this application aims to **understand** the emails.

---

## 2. The Core Problem We Are Solving
- **Information Overload**: Professionals receive hundreds of emails daily. Finding the most important ones or extracting key information (like invoices, tasks, or action items) takes too much manual effort.
- **Context Switching**: Searching for context across multiple long email threads is tedious and inefficient.
- **Lack of Actionable Insights**: Traditional email clients don't summarize, prioritize, or highlight urgent tasks automatically.

---

## 3. Our Solution & Key Features
The Smart Mail Analyzer tackles these problems through:
- **Direct Gmail Integration**: Users log in securely via Google OAuth, and the app fetches their real-time inbox data.
- **Generative AI Analysis (Google Gemini)**: We utilize the Gemini API to analyze email content. This allows us to:
  - Generate 1-sentence summaries of long threads.
  - Determine sentiment (Positive, Negative, Urgent).
  - Extract specific data (e.g., "Find all flight tickets in my inbox").
- **Natural Language "Chat with your Inbox"**: Users can ask questions like *"What did HR say about the new policy?"* and the AI will scan their emails and answer them directly.
- **Modern Web Interface**: Built with Django, HTML, CSS, and Bootstrap for a clean, responsive, and intuitive dashboard.

---

## 4. Technology Stack
Our current architecture is built for rapid development and AI integration:
- **Backend Framework**: Python with Django (MVT architecture).
- **Database**: SQLite (currently) - stores user sessions and OAuth tokens securely.
- **Frontend**: HTML5, CSS3, JavaScript, and Bootstrap for a fast, responsive user interface.
- **AI Integration**: The `google-genai` Python SDK (using `gemini-2.0-flash` or `gemini-1.5-flash`).
- **External APIs**: Gmail API for fetching emails and sending replies.

---

## 5. Project Structure Overview
The Django project is modularized into specific functional "apps":
- `accounts/`: Handles Google OAuth authentication and Custom User Models (storing access/refresh tokens securely).
- `gmail/`: Manages the API connection to Gmail, fetching messages, and rendering the inbox triage view.
- `chat/`: The conversational interface where users can query their emails via an AI chat window.
- `ai/` & `services/`: Dedicated modules for processing data, talking to the Gemini API, and executing heavy AI logic.

---

## 6. Current Status & Next Steps
We have successfully transitioned from a terminal-based prototype to a full web interface. 
**Next steps for our team:**
1. **Fleshing out the Dashboard**: Building visualizations (Chart.js) to show inbox analytics (e.g., top senders, spam risk).
2. **Polishing the AI Chat**: Connecting the frontend chat UI to our backend GenAI Python scripts so users can query their inbox.
3. **Background Processing**: Implementing asynchronous tasks so that AI analysis runs in the background without slowing down the website.

---

## 7. The Vision
Ultimately, Smart Mail Analyzer is not just an email client—it's an **AI Executive Assistant** that triages your inbox, drafts contextual replies, and ensures you never miss an important action item again.
