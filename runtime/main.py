from flask import Flask, send_from_directory, request, jsonify
import os

from runtime import DevineRuntime

app = Flask(__name__)

# path to entities
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ENTITIES_PATH = os.path.join(BASE_DIR, "entities")
DASHBOARD_PATH = os.path.join(BASE_DIR, "dashboard")


# -----------------------------
# Serve Dashboard
# -----------------------------

@app.route("/")
def dashboard():
    return send_from_directory(DASHBOARD_PATH, "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(DASHBOARD_PATH, path)


# -----------------------------
# Awake Entity
# -----------------------------

@app.route("/awake", methods=["POST"])
def awaken_entity():

    data = request.json

    pantheon = data.get("pantheon")
    entity = data.get("entity")

    entity_path = os.path.join(ENTITIES_PATH, pantheon, entity)

    if not os.path.exists(entity_path):
        return jsonify({"error": "Entity not found"}), 404

    runtime = DevineRuntime(entity_path)

    print(f"Entity awakened: {entity}")

    return jsonify({
        "status": "awakened",
        "entity": entity
    })


# -----------------------------
# Chat With Entity
# -----------------------------

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    pantheon = data.get("pantheon")
    entity = data.get("entity")
    message = data.get("message")

    entity_path = os.path.join(ENTITIES_PATH, pantheon, entity)

    if not os.path.exists(entity_path):
        return jsonify({"error": "Entity not found"}), 404

    runtime = DevineRuntime(entity_path)

    response = runtime.cognition.chat(message, runtime.memory)

    return jsonify({
        "entity": entity,
        "response": response
    })


# -----------------------------
# Run Server
# -----------------------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    print("Devines Runtime starting...")
    print(f"Entities path: {ENTITIES_PATH}")

    app.run(
        host="0.0.0.0",
        port=port
    )
