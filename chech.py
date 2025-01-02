import streamlit as st
import base64
import google.generativeai as genai
import requests
import time  # Added for loading animation

# Encoded API keys (new keys encoded)
gemini_encoded_key = "QUl6YVN5QWdDSkpWX0pUdzlhV3BhRUsxdTFyQVRDcVZ0N1FkdmtB"  # New Gemini API Key
news_encoded_key = "MzVkNjIzMGUwMWY5NDI0ZGIwYjdlOWNmZTg1YTUzOWQ="  # News API Key remains unchanged

# Decoding API keys
gemini_api_key = base64.b64decode(gemini_encoded_key).decode('utf-8')
news_api_key = base64.b64decode(news_encoded_key).decode('utf-8')

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Global Styling (including enhancements from the added code)
st.markdown(
    """
    <style>
    /* Global body styling */
    body {
        background: linear-gradient(135deg, #102A2A, #1B1F1F); /* Deep green to charcoal gradient */
        color: #E8E8E8; /* Faded white text */
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
    }

    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        color: #2AFF80; /* Vibrant soft green accent */
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }

    /* Divider styling */
    .fancy-divider {
        border-top: 2px solid #2AFF80; /* Green accent */
        margin: 30px 0;
    }

    /* Button styling */
    .stButton button {
        background: linear-gradient(90deg, #2AFF80, #1BBF5B); /* Gradient green button */
        color: #FFFFFF; /* White text */
        border: none;
        border-radius: 25px;
        padding: 12px 20px;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #1BBF5B, #2AFF80); /* Reverse gradient */
        box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }

    /* Input styling */
    input {
        background: #1C1C1C; /* Sleek dark background */
        color: #FFFFFF; /* Bright white text */
        border: 1px solid #333333;
        border-radius: 15px;
        padding: 12px;
        font-size: 15px;
        box-shadow: inset 0px 2px 4px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    input:hover, input:focus {
        border-color: #2AFF80; /* Green border */
        box-shadow: 0px 0px 5px rgba(42, 255, 128, 0.5); /* Subtle green glow */
    }
    input::placeholder {
        color: #AAAAAA; /* Neutral faded placeholder */
        font-style: italic;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar: Chat History and Developer Info
with st.sidebar:
    st.subheader("Chat History")
    if st.session_state.chat_history:
        for idx, message in enumerate(st.session_state.chat_history):
            st.write(f"{idx+1}. {message}")
    else:
        st.write("No chat history yet.")
    st.markdown("---")
    st.subheader("Developer Info")
    st.write("Created by **Rehan Hussain**.")
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
            st.error(f"API Error: {news_data.get('message', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {e}")
        return None

# NLP functionality for creator-related questions
def handle_creator_query(query):
    keywords = ["creator", "developer", "made you", "created you", "built you", "design", "designer"]
    if any(keyword in query.lower() for keyword in keywords):
        return "I am developed by Rehan Hussain in collaboration with Google technology."
    return None

# Title and Navigation
st.title("Jarvis")
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
menu = ["Ask Jarvis", "Tech News", "About Jarvis"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "Ask Jarvis":
    st.header("Ask Jarvis Anything!")
    user_input = st.text_input("Ask a question... Press Enter to submit.", key="user_input")
    if st.button("Get Response") or user_input:
        with st.spinner("Processing your question..."):
            time.sleep(1)  # Simulating response time
            creator_response = handle_creator_query(user_input)
            response = creator_response if creator_response else generate_jarvis_response(user_input)
            st.session_state.chat_history.append(f"You: {user_input}")
            st.session_state.chat_history.append(f"Jarvis: {response}")
            st.success(f"**Jarvis:** {response}")

elif choice == "Tech News":
    st.header("Latest Tech News")
    news = fetch_news()
    if news:
        for title, description, url in news:
            st.markdown(f"#### [{title}]({url})")
            st.write(description)
            st.markdown("---")

elif choice == "About Jarvis":
    st.header("About Jarvis")
    st.write("Created by **Rehan Hussain** in collaboration with Google.")
    st.write("Jarvis is your futuristic AI assistant, capable of answering questions, fetching tech news, and providing insights.")
	
