import streamlit as st
import base64
import google.generativeai as genai
import requests

# Encoded API keys
gemini_encoded_key = "QUl6YVN5QVFzMnJHY3Z4dVhXalBTT3hwSXliNjdqVU9SRzVVYndV"
news_encoded_key = "MzVkNjIzMGUwMWY5NDI0ZGIwYjdlOWNmZTg1YTUzOWQ="

# Decoding API keys
gemini_api_key = base64.b64decode(gemini_encoded_key).decode('utf-8')
news_api_key = base64.b64decode(news_encoded_key).decode('utf-8')

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Custom styles for a futuristic interface
st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="wide")

st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }
    .stButton button {
        background-color: #1c1c1c;
        color: #00d4ff;
        border: 2px solid #00d4ff;
        border-radius: 10px;
        font-size: 16px;
        padding: 8px 15px;
        transition: 0.3s ease;
    }
    .stButton button:hover {
        background-color: #00d4ff;
        color: #1c1c1c;
    }
    .stTextInput div {
        background-color: #1e1e1e;
        color: #ffffff;
        border-radius: 10px;
        padding: 10px;
    }
    .stSidebar {
        background-color: #121212;
        color: #ffffff;
    }
    .stSidebar .sidebar-content {
        padding: 15px;
    }
    h1, h2, h3, h4 {
        color: #00d4ff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
        news_response = requests.get(news_url)
        news_data = news_response.json()
        if news_data['status'] == 'ok':
            return [(article['title'], article['description'], article['url']) for article in news_data['articles'][:5]]
        else:
            return None
    except Exception as e:
        return f"Error fetching news: {e}"

# NLP functionality for creator-related questions
def handle_creator_query(query):
    keywords = ["creator", "developer", "made you", "created you", "built you"]
    if any(keyword in query.lower() for keyword in keywords):
        return "I am developed by Rehan Hussain in collaboration with Google technology."
    return None

# Jarvis Logo
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.imgur.com/ZkNlQQf.png" alt="Jarvis Logo" style="width: 150px; margin-bottom: 20px;">
    </div>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("🤖 Jarvis AI Assistant")

# Sidebar navigation
menu = ["Ask Jarvis", "Tech News", "About Jarvis"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "Ask Jarvis":
    st.header("Ask Jarvis Anything!")
    user_input = st.text_input("Type your question here (e.g., 'Who is your creator?')")
    if st.button("Get Response"):
        if user_input:
            creator_response = handle_creator_query(user_input)
            if creator_response:
                response = creator_response
            else:
                response = generate_jarvis_response(user_input)
            st.success(f"**Jarvis:** {response}")
        else:
            st.warning("Please enter a question to proceed.")

elif choice == "Tech News":
    st.header("🌐 Latest Tech News")
    news = fetch_news()
    if news:
        for title, description, url in news:
            st.markdown(f"#### [{title}]({url})")
            st.write(description)
            st.markdown("---")
    else:
        st.error("Unable to fetch news at this time.")

elif choice == "About Jarvis":
    st.header("👤 About Jarvis")
    st.write("Created by **Rehan Hussain** in collaboration with Google.")
    st.write(
        """
        Jarvis is your futuristic AI assistant, capable of answering questions,
        fetching the latest technology news, and providing intelligent insights.
        """
    )
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/1y5HY3L.png" alt="AI Graphic" style="width: 300px; margin-top: 20px;">
        </div>
        """,
        unsafe_allow_html=True,
    )
