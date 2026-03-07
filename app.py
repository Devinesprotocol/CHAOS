from flask import Flask, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pantheon")
def pantheon():
    return render_template("pantheon.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/health")
def health():
    return {"status":"alive"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
