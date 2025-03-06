import streamlit as st
import base64
import google.generativeai as genai
import requests

# Encoded API keys (new keys encoded)
gemini_encoded_key = "QUl6YVN5QWdDSkpWX0pUdzlhV3BhRUsxdTFyQVRDcVZ0N1FkdmtB"  # New Gemini API Key
news_encoded_key = "MzVkNjIzMGUwMWY5NDI0ZGIwYjdlOWNmZTg1YTUzOWQ="  # News API Key remains unchanged

# Decoding API keys
gemini_api_key = base64.b64decode(gemini_encoded_key).decode('utf-8')
news_api_key = base64.b64decode(news_encoded_key).decode('utf-8')

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Apply premium UI styling
st.markdown(
    """
    <style>
    /* Premium UI Styling for Streamlit App */
    
    /* Global body styling */
    body {
        background: linear-gradient(135deg, #0a1128, #1a2b54, #263d70);
        color: #e4e6f0;
        font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 16px;
        margin: 0;
        padding: 0;
    }
    
    /* Main content area */
    .main .block-container {
        padding: 2rem;
        border-radius: 15px;
        background: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    h1 {
        font-size: 2.5rem;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    h2, h3, h4 {
        color: #f8fafc;
        margin-top: 1.5rem;
    }
    
    /* Fancy divider */
    .fancy-divider {
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7);
        border-radius: 3px;
        margin: 1.5rem 0;
        opacity: 0.8;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stButton button:hover {
        background: linear-gradient(90deg, #8b5cf6, #6366f1);
        transform: translateY(-3px);
        box-shadow: 0 7px 20px rgba(99, 102, 241, 0.4);
    }
    
    .stButton button:active {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    /* Text input styling */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1rem;
        font-size: 1rem;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
    }
    
    .stTextInput input::placeholder, .stNumberInput input::placeholder, .stTextArea textarea::placeholder {
        color: #94a3b8;
        font-style: italic;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #0f172a, #131e38);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }
    
    /* Sidebar header */
    .sidebar .sidebar-content h1, 
    .sidebar .sidebar-content h2, 
    .sidebar .sidebar-content h3 {
        color: #f8fafc;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar text */
    .sidebar .sidebar-content p, 
    .sidebar .sidebar-content li {
        color: #cbd5e1;
        font-size: 0.95rem;
    }
    
    /* Radio button styling */
    .stRadio > div {
        margin-bottom: 1rem;
    }
    
    .stRadio label {
        background: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stRadio label:hover {
        background: #334155;
        border-color: #6366f1;
    }
    
    .stRadio label[data-baseweb="radio"] input:checked + div {
        background-color: #6366f1;
        border-color: #6366f1;
    }
    
    /* Chat history styling */
    .chat-history {
        background: #1e293b;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 3px solid #6366f1;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1);
        border-radius: 10px;
        border-left: 4px solid #10b981;
        padding: 1rem;
        margin: 1rem 0;
        color: #f8fafc;
    }
    
    /* Error message styling */
    .stError {
        background-color: rgba(239, 68, 68, 0.1);
        border-radius: 10px;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        margin: 1rem 0;
        color: #f8fafc;
    }
    
    /* Links styling */
    a {
        color: #818cf8;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    a:hover {
        color: #a5b4fc;
        text-decoration: underline;
    }
    
    /* News card styling */
    .news-card {
        background: #1e293b;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #334155;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .news-card:hover {
        border-color: #6366f1;
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4b5563;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #6366f1;
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    
    .logo-container img {
        width: 120px;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
        transition: all 0.3s ease;
    }
    
    .logo-container img:hover {
        transform: scale(1.05);
        filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.5));
    }
    
    /* Jarvis response styling */
    .jarvis-response {
        background: linear-gradient(to right, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #8b5cf6;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar: Navigation and Chat History
with st.sidebar:
    st.subheader("Navigation")
    menu = ["Ask Jarvis", "Tech News", "About Jarvis"]
    choice = st.radio("Select a feature:", menu, key="navigation_menu")
    
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    
    st.subheader("Chat History")
    if st.session_state.chat_history:
        for idx, message in enumerate(st.session_state.chat_history):
            st.markdown(f'<div class="chat-history">{idx + 1}. {message}</div>', unsafe_allow_html=True)
    else:
        st.write("No chat history yet.")
    
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    
    st.subheader("Tech Tips")
    tips = [
        "Keep your software up to date",
        "Use strong, unique passwords",
        "Enable two-factor authentication",
        "Backup your important data regularly",
        "Be cautious of suspicious emails and links"
    ]
    for tip in tips:
        st.markdown(f'<div class="tech-tip">• {tip}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    
    st.subheader("Developer Info")
    st.write("Created by **Rehan Hussain**")
    st.write("Contact: rehan9644coc@gmail.com")

# Function to interact with Gemini API
def generate_jarvis_response(query):
    try:
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        response = gemini_model.generate_content(query)
        return response.text
    except Exception as e:
        return f"Jarvis encountered an error: {e}"

# Function to fetch news using News API
def fetch_news():
    news_url = f'https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={news_api_key}'
    try:
        news_response = requests.get(news_url, verify=False)
        news_data = news_response.json()
        if news_data['status'] == 'ok':
            return [(article['title'], article['description'], article['url']) for article in news_data['articles'][:5]]
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

# NLP functionality for creator-related questions
def handle_creator_query(query):
    keywords = ["creator", "developer", "made you", "created you", "built you", "design", "designer"]
    if any(keyword in query.lower() for keyword in keywords):
        return "I am developed by Rehan Hussain in collaboration with Google technology."
    return None

# Jarvis Logo
st.markdown(
    """
    <div class="logo-container">
        <img src="https://i.imgur.com/ZkNlQQf.png" alt="Jarvis Logo">
    </div>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("JARVIS")
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

if choice == "Ask Jarvis":
    st.header("Ask Jarvis Anything!")
    
    user_input = st.text_input("Type your question below:", placeholder="What would you like to know?")
    
    if st.button("Get Response"):
        if user_input:
            st.session_state.chat_history.append(user_input)
            creator_response = handle_creator_query(user_input)
            
            if creator_response:
                response = creator_response
            else:
                response = generate_jarvis_response(user_input)
            
            st.markdown(f'<div class="jarvis-response"><strong>Jarvis:</strong> {response}</div>', unsafe_allow_html=True)

elif choice == "Tech News":
    st.header("Latest Tech News")
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    
    news