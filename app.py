from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_user_data(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT points, invites FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if row:
        return row
    else:
        c.execute("INSERT INTO users (user_id, points, invites) VALUES (?, 0, 0)", (user_id,))
        conn.commit()
        return (0, 0)

@app.route("/get_user", methods=["POST"])
def get_user():
    user_id = request.json["user_id"]
    points, invites = get_user_data(user_id)
    return jsonify({"points": points, "invites": invites})

@app.route("/quiz", methods=["POST"])
def quiz():
    user_id = request.json["user_id"]
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("UPDATE users SET points = points + 10 WHERE user_id=?", (user_id,))
    conn.commit()
    return jsonify({"message": "10 очков за викторину начислено"})

@app.route("/invite", methods=["POST"])
def invite():
    user_id = request.json["user_id"]
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("UPDATE users SET points = points + 5, invites = invites + 1 WHERE user_id=?", (user_id,))
    conn.commit()
    return jsonify({"message": "5 очков и 1 приглашение начислены"})

if __name__ == "__main__":
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    points INTEGER DEFAULT 0,
                    invites INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()
    app.run(host="0.0.0.0", port=5000)
