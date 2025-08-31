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
    /* Global body styling */
    body {
        background: linear-gradient(135deg, #0F2027, #203A43, #2C5364);
        color: #F3904F
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
        margin: 0;
        padding: 0;
    }

    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        color: #56CCF2;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }

    /* Fancy divider */
    .fancy-divider {
        border-top: 2px solid #56CCF2;
        margin: 30px 0;
    }

    /* Button styling */
    .stButton button {
        background: linear-gradient(90deg, #1F4037, #99F2C8);
        color: #FFFFFF;
        border: none;
        border-radius: 25px;
        padding: 12px 20px;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #99F2C8, #1F4037);
        box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }

    /* Text input styling */
    input {
        background: #203A43; /* Updated background for better contrast */
        color: #E8E8E8;
        border: 1px solid #333333;
        border-radius: 15px;
        padding: 12px;
        font-size: 15px;
        box-shadow: inset 0px 2px 4px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    input::placeholder {
        color: #D3D3D3; /* Adjusted placeholder color */
        font-style: italic;
    }

/* Sidebar styling */
.stSidebar {
   background: linear-gradient(135deg, #1F4037, #1C1C1C);
        color: #E8E8E8;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.2);
}

/* Navigation Header */
.stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar p {
    color: #FFFFFF; /* Set text to white for high contrast */
    font-size: 16px; /* Adjust font size for readability */
    font-weight: bold;
}

/* Navigation Text Styling */
.stSidebar .radio > label {
    color: #FFFFFF; /* Text color for radio labels */
    font-weight: bold;
    font-size: 14px;
    margin-bottom: 8px;
    padding: 8px 12px;
    border-radius: 8px;
    background: #2A2A40; /* Slightly lighter background for radio buttons */
    cursor: pointer;
    transition: all 0.3s ease;
}

.stSidebar .radio > label:hover {
    background: #44446A; /* Slightly darker on hover */
    color: #FFFFFF; /* Keep text visible */
}

.stSidebar .radio > label > input {
    display: none; /* Hide default radio button */
}

.stSidebar .radio > label.selected {
    background: #5656A1; /* Highlight for selected option */
    color: #FFFFFF; /* Keep text color visible */
}


    /* Chat history styling */
    .chat-history {
        background: #4b4371
        border-radius: 12px;
        padding: 15px;
        box-shadow: inset 0px 2px 4px rgba(0, 0, 0, 0.2);
        color: #FFFFFF;
    }

    /* Links styling */
    a {
        color: #56CCF2;
        text-decoration: none;
        font-weight: bold;
    }
    a:hover {
        text-decoration: underline;
        color: #99F2C8;
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
    st.write("Contact: Email us not availble ")

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
st.title("JARVIS")

if choice == "Ask Jarvis":
    st.header("Ask Jarvis Anything!")
    user_input = st.text_input("Type your question below:")
    if st.button("Submit"):
        if user_input:
            st.session_state.chat_history.append(user_input)  # Append only user questions
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
    st.write("""
        """
    )
