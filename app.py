from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "name": "DEVINES",
        "protocol": "Devines Protocol",
        "core": "CHAOS",
        "status": "active"
    })

# REQUIRED for Render
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/ping")
def ping():
    return "pong"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
