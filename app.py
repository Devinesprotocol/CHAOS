from flask import Flask, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status":"alive"})

@app.route("/api")
def api():
    return jsonify({
        "core":"CHAOS",
        "system":"Devines Protocol"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)
