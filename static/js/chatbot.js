/**
 * eSociety Chatbot JS Interface
 */

// Maintain conversation history in memory
let chatHistory = [];

function toggleChatbot() {
    const chatWindow = document.getElementById('chatbot-window');
    const toggleBtnIcon = document.querySelector('#chatbot-toggle span');
    if (chatWindow.classList.contains('hidden')) {
        chatWindow.classList.remove('hidden');
        chatWindow.classList.add('flex');
        toggleBtnIcon.textContent = 'expand_more';
        
        // Show initial options if history is empty
        if (chatHistory.length === 0) {
            showInitialOptions();
        }
    } else {
        chatWindow.classList.add('hidden');
        chatWindow.classList.remove('flex');
        toggleBtnIcon.textContent = 'chat';
    }
}

function showInitialOptions() {
    const messagesContainer = document.getElementById('chatbot-messages');
    
    const options = [
        { text: "💰 Check My Bills", value: "Show my pending maintenance bills and invoices" },
        { text: "🏢 Book a Facility", value: "I want to book a facility like the Gym or Hall. How do I pay for it?" },
        { text: "📅 My Bookings", value: "Show my current facility bookings and their payment status" },
        { text: "📝 File a Complaint", value: "I have an issue with the society services, I want to file a complaint" }
    ];

    const optionsDiv = document.createElement('div');
    optionsDiv.className = 'flex flex-wrap gap-2 mt-2 initial-options';
    
    options.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = 'bg-white border border-primary/20 text-primary text-[11px] font-bold px-3 py-2 rounded-xl hover:bg-primary hover:text-white transition-all shadow-sm';
        btn.textContent = opt.text;
        btn.onclick = () => {
            const inputField = document.getElementById('chatbot-input');
            inputField.value = opt.value;
            document.getElementById('chatbot-form').dispatchEvent(new Event('submit'));
            optionsDiv.remove(); // Remove options after one is clicked
        };
        optionsDiv.appendChild(btn);
    });
    
    messagesContainer.appendChild(optionsDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function handleChatbotSubmit(event) {
    event.preventDefault();
    const inputField = document.getElementById('chatbot-input');
    const message = inputField.value.trim();
    if (!message) return;

    const messagesContainer = document.getElementById('chatbot-messages');

    // Add user message to UI
    const userMsgDiv = document.createElement('div');
    userMsgDiv.className = 'self-end max-w-[85%]';
    userMsgDiv.innerHTML = `<div class="bg-[#5a5ae6] text-white p-3 rounded-2xl rounded-tr-sm shadow-sm">${message.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</div>`;
    messagesContainer.appendChild(userMsgDiv);
    inputField.value = '';
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Save to history
    chatHistory.push({ role: 'user', content: message });

    // Add loading indicator
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'self-start max-w-[85%] loading-msg';
    loadingDiv.innerHTML = `<div class="bg-white border border-gray-100 text-gray-500 p-3 rounded-2xl rounded-tl-sm shadow-sm flex items-center gap-2"><span class="material-symbols-outlined animate-spin" style="font-size:16px;">progress_activity</span> Thinking...</div>`;
    messagesContainer.appendChild(loadingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    try {
        const csrftoken = getCookie('csrftoken');
        const response = await fetch('/api/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            // Send both current message AND context
            body: JSON.stringify({ 
                message: message,
                history: chatHistory.slice(0, -1) // Send previous history (excluding current msg which backend handles)
            })
        });

        const data = await response.json();
        
        // Remove loading
        if (loadingDiv.parentNode) messagesContainer.removeChild(loadingDiv);

        // Add bot response
        const botMsgDiv = document.createElement('div');
        botMsgDiv.className = 'self-start max-w-[85%]';
        
        const innerDiv = document.createElement('div');
        innerDiv.className = 'bg-white border border-gray-100 text-gray-800 p-3 rounded-2xl rounded-tl-sm shadow-sm whitespace-pre-wrap';
        
        let rawText = data.response || "Sorry, I couldn't process that.";
        
        // Save bot response to history
        chatHistory.push({ role: 'assistant', content: rawText });
        
        // Keep history size manageable (last 40 turns max)
        if (chatHistory.length > 40) {
            chatHistory = chatHistory.slice(-40);
        }

        if (typeof marked !== 'undefined') {
            // Use marked library loaded in base.html
            marked.use({ breaks: true });
            innerDiv.innerHTML = marked.parse(rawText);
            
            // Apply lightweight typography classes to generated elements
            // since Tailwind resets them by default.
            innerDiv.querySelectorAll('ul').forEach(ul => ul.className = 'list-disc pl-5 mb-2');
            innerDiv.querySelectorAll('p').forEach(p => p.className = 'mb-2 last:mb-0');
        } else {
            // Fallback
            innerDiv.textContent = rawText;
        }
        
        botMsgDiv.appendChild(innerDiv);
        
        messagesContainer.appendChild(botMsgDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

    } catch (error) {
        if (loadingDiv.parentNode) messagesContainer.removeChild(loadingDiv);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'self-start max-w-[85%]';
        errorDiv.innerHTML = `<div class="bg-[#ffdad6] text-[#93000a] p-3 rounded-2xl rounded-tl-sm shadow-sm">Connection error. Please try again later.</div>`;
        messagesContainer.appendChild(errorDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}
