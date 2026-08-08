# AI Study Assistant

A small Flask web app that helps students study: ask questions, get topic summaries,
or generate a 3-question practice quiz. Powered by the OpenAI API.

**Live demo:** _add your deployed URL here after deploying_

## Tech stack
- Backend: Python, Flask
- Frontend: HTML, CSS, vanilla JavaScript (fetch API)
- AI: OpenAI Chat Completions API
- Deployment: Render / Railway (gunicorn)

## Run locally

1. Clone this repo and enter the folder:
   ```bash
   git clone <your-repo-url>
   cd study-assistant
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and paste your key from https://platform.openai.com/api-keys

4. Load the env var and run the app:
   ```bash
   export $(cat .env | xargs)    # Windows: use `set` per line instead, or a tool like python-dotenv
   python app.py
   ```

5. Open http://localhost:5000 in your browser.

## Deploy (Render.com — free tier)

1. Push this folder to a new GitHub repository.
2. Go to https://render.com → New → Web Service → connect your GitHub repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. In the Environment tab, add `OPENAI_API_KEY` with your key.
6. Deploy. Render gives you a public URL — put it in this README and on your resume.

## Project structure
```
study-assistant/
├── app.py               # Flask backend + API routes
├── templates/
│   └── index.html       # Chat UI
├── static/
│   └── style.css         # Styling
├── requirements.txt
├── Procfile              # tells Render/Railway how to start the app
├── .env.example
└── .gitignore
```

## Notes
- The API key is never hardcoded — it's read from an environment variable both
  locally (`.env`, not committed) and in production (set in the host's dashboard).
- Errors from the AI API are caught and logged server-side; the user only sees a
  clean error message, never raw exception details.
