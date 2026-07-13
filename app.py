from flask import Flask, jsonify, request

app = Flask(__name__)

_todos = {}
_next_id = 1


@app.get("/health")
def health():
    return {"status": "ok"}, 200


@app.get("/todos")
def list_todos():
    return jsonify(list(_todos.values())), 200


@app.post("/todos")
def create_todo():
    global _next_id
    body = request.get_json(silent=True) or {}
    title = body.get("title")
    if not title:
        return jsonify(error="title is required"), 400

    todo = {"id": _next_id, "title": title, "done": False}
    _todos[_next_id] = todo
    _next_id += 1
    return jsonify(todo), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)