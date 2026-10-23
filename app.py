import os
import sqlite3

from flask import Flask, g, jsonify, request, send_from_directory

DB_PATH = os.environ.get("TODO_DB", os.path.join(os.path.dirname(__file__), "todos.db"))

app = Flask(__name__, static_folder="static", static_url_path="/static")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS todos ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "text TEXT NOT NULL,"
            "done INTEGER NOT NULL DEFAULT 0)"
        )


def row_to_dict(row):
    return {"id": row["id"], "text": row["text"], "done": bool(row["done"])}


def clean_text(value):
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/todos")
def list_todos():
    rows = get_db().execute("SELECT * FROM todos ORDER BY id").fetchall()
    return jsonify([row_to_dict(r) for r in rows])


@app.post("/api/todos")
def create_todo():
    data = request.get_json(silent=True) or {}
    text = clean_text(data.get("text"))
    if text is None:
        return jsonify(error="text darf nicht leer sein"), 400
    db = get_db()
    cur = db.execute("INSERT INTO todos (text) VALUES (?)", (text,))
    db.commit()
    row = db.execute("SELECT * FROM todos WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(row_to_dict(row)), 201


@app.patch("/api/todos/<int:todo_id>")
def update_todo(todo_id):
    data = request.get_json(silent=True) or {}
    db = get_db()
    row = db.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if row is None:
        return jsonify(error="nicht gefunden"), 404

    text = row["text"]
    done = row["done"]
    if "text" in data:
        text = clean_text(data["text"])
        if text is None:
            return jsonify(error="text darf nicht leer sein"), 400
    if "done" in data:
        if not isinstance(data["done"], bool):
            return jsonify(error="done muss ein Boolean sein"), 400
        done = int(data["done"])

    db.execute("UPDATE todos SET text = ?, done = ? WHERE id = ?", (text, done, todo_id))
    db.commit()
    row = db.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    return jsonify(row_to_dict(row))


@app.delete("/api/todos/<int:todo_id>")
def delete_todo(todo_id):
    db = get_db()
    cur = db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify(error="nicht gefunden"), 404
    return "", 204


init_db()

if __name__ == "__main__":
    app.run(debug=True)
