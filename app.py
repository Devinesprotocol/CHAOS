from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os

from runtime.entity_loader import EntityLoader
from runtime.cognition_engine import CognitionEngine

app = Flask(__name__)
CORS(app)

loader = EntityLoader()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pantheon")
@app.route("/pantheon.html")
def pantheon():
    return render_template("pantheon.html")


@app.route("/chat", methods=["GET", "POST"])
@app.route("/chat.html", methods=["GET"])
def chat():
    if request.method == "GET":
        return render_template("chat.html")

    try:
        data = request.get_json(silent=True) or {}

        pantheon = (data.get("pantheon") or "greek").strip().lower()
        entity = (data.get("entity") or "CHAOS").strip().upper()
        message = (data.get("message") or "").strip()

        if not message:
            return jsonify({"error": "Message is required."}), 400

        entity_payload = loader.load_entity(pantheon, entity)
        engine = CognitionEngine(entity_payload)
        result = engine.respond(message)

        return jsonify({
            "entity": result.get("entity", entity),
            "response": result.get("reply", ""),
            "history_count": result.get("history_count", 0)
        })

    except FileNotFoundError:
        return jsonify({"error": "Entity not found."}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route("/health")
def health():
    return {"status": "alive"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
