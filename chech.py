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
st.markdown(
    """
    <style>
    /* Global body styling for dark mode */
    body {
        background: #121212; /* Dark background */
        color: #E0E0E0; /* Light text color */
        font-family: 'Roboto', sans-serif;
    }
    
    /* Styling for headers */
    h1, h2, h3, h4, h5, h6 {
        color: #00d4ff; /* Neon blue for titles */
    }
    
    /* Button styling */
    .stButton button {
        background-color: #1F1F1F; /* Dark button background */
        color: #00d4ff; /* Neon blue text */
        border: 2px solid #00d4ff;
        border-radius: 8px;
        padding: 10px 15px;
        font-size: 16px;
        transition: 0.3s ease;
    }
    .stButton button:hover {
        background-color: #00d4ff; /* Neon blue hover effect */
        color: #1F1F1F; /* Invert text and background */
    }
    
    /* Text input styling */
    input {
        background-color: #1F1F1F; /* Dark background for text input */
        color: #E0E0E0; /* Light text color */
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
    }
    input::placeholder {
        color: #888888; /* Light gray placeholder text */
    }
    
    /* Sidebar styling */
    .stSidebar {
        background-color: #1C1C1C; /* Dark sidebar */
        color: #E0E0E0; /* Light text */
        padding: 15px;
    }
    
    /* Sidebar title and text */
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar p {
        color: #00d4ff; /* Neon blue for sidebar titles */
    }
    
    /* Chat history box */
    .chat-history {
        background-color: #1F1F1F; /* Dark background */
        color: #E0E0E0; /* Light text */
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #333333;
    }
    
    /* Links styling */
    a {
        color: #00d4ff;
        text-decoration: none;
    }
    a:hover {
        color: #1E90FF; /* Slightly lighter blue on hover */
    }
    
    /* Divider styling */
    .fancy-divider {
        border-top: 2px solid #00d4ff;
        margin: 20px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Updating the main app content with consistent colors
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.header("Ask Jarvis Anything!")
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# Sidebar: Developer Info and Tech Tips
with st.sidebar:
    st.subheader("Tech Tips")
    tips = [
        "Keep your software up to date.",
        "Use strong, unique passwords.",
        "Enable two-factor authentication.",
        "Avoid clicking on suspicious links.",
        "Regularly back up your data.",
        "Use antivirus software.",
    ]
    for tip in tips:
        st.write(f"- {tip}")

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
        # Disabling SSL verification temporarily (for troubleshooting)
        news_response = requests.get(news_url, verify=False)
        
        # Parse the JSON response
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

# Jarvis Logo
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.imgur.com/ZkNlQQf.png" alt="Jarvis Logo" style="width: 150px; margin-bottom: 20px;">
    </div>
    """,
    unsafe_allow_html=True,
)

# Title without emoji
st.title("Jarvis")

# Fancy Divider
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# Sidebar navigation
menu = ["Ask Jarvis", "Tech News", "About Jarvis"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "Ask Jarvis":
    st.header("Ask Jarvis Anything!")
    
    # User question input box
    user_input = st.text_input("Ask a question... Press Enter to submit.", key="user_input")
    
    # Button to generate response
    if st.button("Get Response"):
        if user_input:
            creator_response = handle_creator_query(user_input)
            if creator_response:
                response = creator_response
            else:
                response = generate_jarvis_response(user_input)
            st.success(f"**Jarvis:** {response}")
    
    # Handle the Enter key press for response
    if user_input:
        creator_response = handle_creator_query(user_input)
        if creator_response:
            response = creator_response
        else:
            response = generate_jarvis_response(user_input)
        st.success(f"**Jarvis:** {response}")

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
    st.header("👾 About Jarvis")
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
