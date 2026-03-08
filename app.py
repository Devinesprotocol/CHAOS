from flask import Flask, request, jsonify, render_template

from runtime.entity_loader import EntityLoader
from runtime.cognition_engine import CognitionEngine

app = Flask(__name__)

loader = EntityLoader()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pantheon/greek")
def greek():
    return render_template("greek.html")


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.json

    pantheon = data.get("pantheon", "greek")
    entity = data.get("entity", "CHAOS")
    message = data.get("message", "")

    try:
        # Load Devines being
        entity_payload = loader.load_entity(pantheon, entity)

        # Initialize cognition engine
        engine = CognitionEngine(entity_payload)

        # Generate response
        response = engine.respond(message)

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
