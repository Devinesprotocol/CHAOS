import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return {"system": "Devines Protocol", "core": "CHAOS"}

@app.route("/health")
def health():
    return {"status": "alive"}

@app.route("/ping")
def ping():
    return {"ping": "pong"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
