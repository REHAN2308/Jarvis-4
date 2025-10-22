# Setup Instructions for Jarvis Streamlit App

## Securing API Keys

This application now uses environment variables to secure API keys. Follow the instructions below:

### Option 1: Using Streamlit Secrets (Recommended for Streamlit Cloud)

1. Create a `.streamlit` folder in your project root (if it doesn't exist)
2. Create a file named `secrets.toml` inside the `.streamlit` folder
3. Add your API keys to `secrets.toml`:

```toml
OPENROUTER_API_KEY = "your-actual-openrouter-api-key"
NEWS_API_KEY = "your-actual-news-api-key"
```

4. **IMPORTANT**: Never commit `secrets.toml` to version control (it's already in `.gitignore`)

### Option 2: Using Environment Variables (For Local Development)

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your actual API keys:
   ```
   OPENROUTER_API_KEY=your-actual-openrouter-api-key
   NEWS_API_KEY=your-actual-news-api-key
   ```

3. Install python-dotenv if not already installed:
   ```bash
   pip install python-dotenv
   ```

4. Load environment variables before running (add to `chech.py` if using .env):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

### Option 3: Set Environment Variables in PowerShell

For Windows PowerShell, set environment variables before running:

```powershell
$env:OPENROUTER_API_KEY="your-actual-openrouter-api-key"
$env:NEWS_API_KEY="your-actual-news-api-key"
streamlit run chech.py
```

### For Streamlit Cloud Deployment

1. Go to your app settings on Streamlit Cloud
2. Navigate to "Secrets" section
3. Add your secrets in TOML format:

```toml
OPENROUTER_API_KEY = "your-actual-openrouter-api-key"
NEWS_API_KEY = "your-actual-news-api-key"
```

## Getting API Keys

- **OpenRouter API Key**: Sign up at [https://openrouter.ai/](https://openrouter.ai/)
- **News API Key**: Sign up at [https://newsapi.org/](https://newsapi.org/)

## Running the App

```bash
streamlit run chech.py
```

## Security Notes

- Never commit `.env` or `.streamlit/secrets.toml` files
- Never hardcode API keys in your source code
- Use `.gitignore` to prevent accidental commits
- Rotate your API keys if they are ever exposed
