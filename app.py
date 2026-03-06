from flask import Flask, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {"agent": "CHAOS", "status": "active"}

@app.route("/health")
def health():
    return {"status": "alive", "agent": "CHAOS"}

@app.route("/message", methods=["POST"])
def message():
    data = request.json
    user_message = data.get("message", "")

    return {
        "agent": "CHAOS",
        "reply": f"Received: {user_message}"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
