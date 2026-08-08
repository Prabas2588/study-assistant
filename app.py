import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

# The API key is read from an environment variable.
# Locally: put it in a .env file (see .env.example) and load it with python-dotenv.
# In production (Render/Railway): set it in the dashboard's Environment Variables section.
# NOTE: client is created lazily so the app can still boot (and show a clean error)
# even if the key hasn't been set yet.
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY") or "not-set")

MODEL = "gpt-4o-mini"  # cheap + fast; swap for any chat model your key supports

SYSTEM_PROMPTS = {
    "ask": (
        "You are a friendly, patient study assistant for a college student. "
        "Explain concepts simply, use short paragraphs, and give a concrete example when useful."
    ),
    "summarize": (
        "You are a study assistant. Summarize the topic the student gives you into "
        "5-7 concise bullet points suitable for last-minute exam revision."
    ),
    "quiz": (
        "You are a study assistant. Generate exactly 3 short practice questions "
        "(no answers) on the topic the student gives you, numbered 1-3."
    ),
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()
    mode = data.get("mode", "ask")

    if not question:
        return jsonify({"error": "Please type a question or topic."}), 400
    if mode not in SYSTEM_PROMPTS:
        mode = "ask"
    if not os.environ.get("OPENAI_API_KEY"):
        return jsonify({"error": "Server is missing OPENAI_API_KEY."}), 500

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPTS[mode]},
                {"role": "user", "content": question},
            ],
            max_tokens=500,
        )
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        # Never leak the raw exception (could contain key info) - log it, return a clean message
        app.logger.error(f"OpenAI API error: {e}")
        return jsonify({"error": "Something went wrong talking to the AI service. Please try again."}), 502


if __name__ == "__main__":
    # debug=True is fine locally; Render/Railway will use gunicorn instead (see Procfile)
    app.run(debug=True, port=5000)
