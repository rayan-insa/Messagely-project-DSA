from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulated database
conversations = [
    {"id": 1, "name": "John Doe"},
    {"id": 2, "name": "Group: Friends"},
]

messages = {
    1: [
        {"sender": "John Doe", "content": "Hey there!", "timestamp": "10:30"},
        {"sender": "You", "content": "Hello!", "timestamp": "10:31"},
    ],
    2: [
        {"sender": "Alice", "content": "Hi everyone!", "timestamp": "09:00"},
        {"sender": "You", "content": "Good morning!", "timestamp": "09:05"},
    ],
}

@app.route("/")
def home():
    return render_template("home.html", conversations=conversations)

@app.route("/chat/<int:chat_id>")
def chat(chat_id):
    chat_name = next(c["name"] for c in conversations if c["id"] == chat_id)
    return render_template("chat.html", chat_name=chat_name, messages=messages[chat_id], chat_id=chat_id, current_user="You")

@app.route("/chat/<int:chat_id>/send", methods=["POST"])
def send_message(chat_id):
    content = request.form["message"]
    messages[chat_id].append({"sender": "You", "content": content, "timestamp": "12:00"})
    return redirect(url_for("chat", chat_id=chat_id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
