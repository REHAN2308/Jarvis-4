import streamlit as st
import base64
import google.generativeai as genai
import requests

# Encoded API keys (new keys encoded)
gemini_encoded_key = "QUl6YVN5QWdDSkpWX0pUdzlhV3BhRUsxdTFyQVRDcVZ0N1FkdmtB" # New Gemini API Key
news_encoded_key = "MzVkNjIzMGUwMWY5NDI0ZGIwYjdlOWNmZTg1YTUzOWQ=" # News API Key remains unchanged

# Decoding API keys
gemini_api_key = base64.b64decode(gemini_encoded_key).decode('utf-8')
news_api_key = base64.b64decode(news_encoded_key).decode('utf-8')

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Custom CSS styling with your new colors
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f8f9fa;
        }
        .stTitle h1 {
            color: #F3904F !important;
            font-weight: bold;
            text-align: center;
        }
        .stHeader h2 {
            color: #4b4371 !important;
            font-weight: 600;
        }
        .stSubheader {
            color: #F3904F !important;
            font-weight: 500;
        }
        .stRadio > label {
            color: #4b4371 !important;
            font-weight: 500;
        }
        .stButton > button {
            background-color: #F3904F !important;
            color: white !important;
            border: none !important;
            border-radius: 5px !important;
            font-weight: 500 !important;
        }
        .stButton > button:hover {
            background-color: #d17a42 !important;
        }
        .stTextInput > div > div > input {
            border-color: #4b4371 !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #F3904F !important;
            box-shadow: 0 0 0 2px rgba(243, 144, 79, 0.2) !important;
        }
        .sidebar .stSubheader {
            color: #F3904F !important;
        }
        .success {
            background-color: rgba(75, 67, 113, 0.1) !important;
            border-left: 4px solid #4b4371 !important;
        }
        .css-1v3fvcr {
            border-right: 2px solid #F3904F !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar: Chat History and Navigation
with st.sidebar:
    st.subheader("Navigation")
    menu = ["Ask Jarvis", "Tech News", "About Jarvis"]
    choice = st.radio("Select a feature:", menu, key="navigation_menu")
    
    st.subheader("Chat History")
    if st.session_state.chat_history:
        for idx, message in enumerate(st.session_state.chat_history):
            st.write(f"{idx + 1}. {message}")
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
            return None
    except requests.exceptions.RequestException as e:
        return None

# Title
st.title("🤖 JARVIS")

if choice == "Ask Jarvis":
    st.header("Ask Jarvis Anything!")
    user_input = st.text_input("Type your question below:")
    
    if st.button("Submit"):
        if user_input:
            st.session_state.chat_history.append(user_input) # Append only user questions
            response = generate_jarvis_response(user_input)
            st.success(f"**Jarvis:** {response}")

elif choice == "Tech News":
    st.header("Latest Tech News")
    news = fetch_news()
    if news:
        for title, description, url in news:
            st.markdown(f"### [{title}]({url})")
            st.write(description)
            st.markdown("---")
    else:
        st.error("Unable to fetch news at this time.")

elif choice == "About Jarvis":
    st.header("About Jarvis")
    st.write("Created by **Rehan Hussain** in collaboration with Google.")
    st.write(
        """
        Jarvis is your futuristic AI assistant, capable of answering questions,
        fetching the latest technology news, and providing intelligent insights.
        """
    )
