from flask import Flask, render_template, request, jsonify
from insertListener import insert_listener, move_files
app = Flask(__name__, template_folder="web/templates", static_folder="web/static")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/action/<command>", methods=["POST"])
def handle_action(command):
    if command == "move":
        print("Move function triggered")
        insert_listener()

    elif command == "stream":
        # Call your Python function for "stream"
        print("Stream function triggered")
    elif command == "settings":
        # Call your Python function for "settings"
        print("Settings function triggered")

    return jsonify({"status": "success", "command": command})



if __name__ == "__main__":
    app.run(debug=True)
