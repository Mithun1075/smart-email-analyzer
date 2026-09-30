/**
 * Smart Email Analyzer - SPA Frontend Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatMessages = document.getElementById('chatMessages');
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const authBtn = document.getElementById('authBtn');
    const clearChatBtn = document.getElementById('clearChatBtn');
    const docUploadTrigger = document.getElementById('docUploadTrigger');
    const docUploadInput = document.getElementById('docUploadInput');
    const docIndicatorContainer = document.getElementById('docIndicatorContainer');
    const csrfTokenElem = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfTokenElem ? csrfTokenElem.value : '';

    // Theme Toggle Logic
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeToggleText = document.getElementById('themeToggleText');

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('sea_theme', theme);
        if (themeToggleBtn && themeToggleText) {
            const icon = themeToggleBtn.querySelector('i');
            if (theme === 'dark') {
                themeToggleText.textContent = 'Light';
                if (icon) icon.className = 'fa-solid fa-sun';
            } else {
                themeToggleText.textContent = 'Dark';
                if (icon) icon.className = 'fa-solid fa-moon';
            }
        }
    }

    // Read active theme set by head script or default
    const activeTheme = document.documentElement.getAttribute('data-theme') || 
                        localStorage.getItem('sea_theme') || 
                        (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    
    setTheme(activeTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            setTheme(currentTheme === 'dark' ? 'light' : 'dark');
        });
    }

    // Scroll chat to bottom on load
    function scrollToBottom() {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    scrollToBottom();

    // Chat Form Submit
    if (chatForm) {
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const text = userInput.value.trim();
            if (!text) return;
            submitMessage(text);
            userInput.value = '';
        });
    }

    async function submitMessage(messageText) {
        // Append User Message
        appendUserMessage(messageText);

        // Append Typing Indicator
        const typingMsgId = appendTypingIndicator();

        try {
            const res = await fetch('/api/send_message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ message: messageText })
            });

            const data = await res.json();

            // Remove typing indicator
            removeMessageById(typingMsgId);

            if (res.ok && data.response) {
                appendAssistantMessage(data.response);
            } else {
                appendAssistantMessage(`⚠️ Error processing request: ${data.error || 'Unknown error'}`);
            }

        } catch (err) {
            removeMessageById(typingMsgId);
            appendAssistantMessage(`⚠️ Connection Error: Failed to reach backend API.`);
            console.error(err);
        }
    }

    function appendUserMessage(text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'chat-message user-message';
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-user"></i></div>
            <div class="message-content">
                <div class="sender-name">You</div>
                <div class="message-body">${escapeHtml(text)}</div>
            </div>
        `;
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function appendAssistantMessage(text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'chat-message assistant-message';
        let formattedText = formatMarkdown(text);

        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="message-content">
                <div class="sender-name">Smart Email Assistant</div>
                <div class="message-body">${formattedText}</div>
            </div>
        `;
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function appendTypingIndicator() {
        const msgId = 'typing_' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.id = msgId;
        msgDiv.className = 'chat-message assistant-message';
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="message-content">
                <div class="sender-name">Analyzing Intent & Gmail Data...</div>
                <div class="message-body"><i class="fa-solid fa-spinner fa-spin"></i> Gemini & MCP retrieving email details...</div>
            </div>
        `;
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
        return msgId;
    }

    function removeMessageById(id) {
        const elem = document.getElementById(id);
        if (elem) elem.remove();
    }

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    function formatMarkdown(text) {
        if (!text) return '';
        let html = text
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/```text([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
            .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
            .replace(/\n/g, '<br>');
        return html;
    }

    const headerNewChatBtn = document.getElementById('headerNewChatBtn');
    const newChatBtn = document.getElementById('newChatBtn');

    async function handleNewChat(btnElem) {
        if (!btnElem || btnElem.disabled) return;
        const iconElem = btnElem.querySelector('i');
        const originalIconClass = iconElem ? iconElem.className : 'fa-solid fa-plus';
        
        btnElem.disabled = true;
        if (iconElem) iconElem.className = 'fa-solid fa-spinner fa-spin';

        try {
            const res = await fetch('/api/clear_chat/', {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken }
            });
            if (res.ok) {
                if (chatMessages) {
                    chatMessages.innerHTML = `
                        <div class="chat-message assistant-message">
                            <div class="avatar"><i class="fa-solid fa-robot"></i></div>
                            <div class="message-content">
                                <div class="sender-name">Smart Email Assistant</div>
                                <div class="message-body">
                                    <p>Hello! I'm your <strong>Smart Email Analyzer</strong> assistant powered by Gemini AI and Model Context Protocol (MCP).</p>
                                    <p>I understand natural language phrasing with <em>no strict command syntax required</em>. Ask me to search your emails, summarize threads, find attachments, or analyze documents.</p>
                                    <p>How can I help you analyze your Gmail today?</p>
                                </div>
                            </div>
                        </div>
                    `;
                }
            }
        } catch (err) {
            console.error('New chat error:', err);
        } finally {
            btnElem.disabled = false;
            if (iconElem) iconElem.className = originalIconClass;
        }
    }

    if (headerNewChatBtn) {
        headerNewChatBtn.addEventListener('click', () => handleNewChat(headerNewChatBtn));
    }
    if (newChatBtn) {
        newChatBtn.addEventListener('click', () => handleNewChat(newChatBtn));
    }

    // Document Upload Logic
    if (docUploadTrigger && docUploadInput) {
        docUploadTrigger.addEventListener('click', () => {
            docUploadInput.click();
        });

        docUploadInput.addEventListener('change', async function() {
            if (this.files && this.files[0]) {
                const file = this.files[0];
                const formData = new FormData();
                formData.append('document', file);

                appendAssistantMessage(`Uploading document <strong>${escapeHtml(file.name)}</strong>... <i class="fa-solid fa-spinner fa-spin"></i>`);

                try {
                    const res = await fetch('/api/upload_document/', {
                        method: 'POST',
                        headers: { 'X-CSRFToken': csrfToken },
                        body: formData
                    });
                    const data = await res.json();
                    if (res.ok) {
                        if (docIndicatorContainer) {
                            docIndicatorContainer.innerHTML = `
                                <div class="doc-badge" id="currentDocBadge">
                                    <i class="fa-solid fa-file-lines me-1"></i> 
                                    <span id="docName">${escapeHtml(data.filename)}</span>
                                    <button type="button" class="btn-close-doc" id="clearDocBtn" title="Remove document">
                                        <i class="fa-solid fa-circle-xmark"></i>
                                    </button>
                                </div>
                            `;
                            attachClearDocEvent();
                        }
                        appendAssistantMessage(`Successfully uploaded <strong>${escapeHtml(data.filename)}</strong>. I am now in Document Analysis mode.`);
                    } else {
                        appendAssistantMessage(`⚠️ Failed to upload document: ${data.error || 'Unsupported file type'}`);
                    }
                } catch (err) {
                    appendAssistantMessage(`⚠️ Document upload failed due to network error.`);
                }
                docUploadInput.value = '';
            }
        });
    }

    function attachClearDocEvent() {
        const clearDocBtn = document.getElementById('clearDocBtn');
        if (clearDocBtn) {
            clearDocBtn.addEventListener('click', async () => {
                try {
                    const res = await fetch('/api/clear_document/', {
                        method: 'POST',
                        headers: { 'X-CSRFToken': csrfToken }
                    });
                    if (res.ok) {
                        if (docIndicatorContainer) docIndicatorContainer.innerHTML = '';
                        appendAssistantMessage('Document cleared. Switched back to Gmail Inbox mode!');
                    }
                } catch (err) {
                    console.error('Clear document error:', err);
                }
            });
        }
    }
    attachClearDocEvent();

});
