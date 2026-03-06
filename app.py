from flask import Flask, jsonify

app = Flask(__name__)

# Root endpoint
@app.route("/")
def home():
    return jsonify({
        "name": "DEVINES",
        "protocol": "Devines Protocol",
        "status": "active",
        "core": "CHAOS",
        "message": "Devines Core is alive"
    })


# Health check endpoint (REQUIRED for Render)
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


# Optional: ping endpoint
@app.route("/ping")
def ping():
    return "pong"


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
