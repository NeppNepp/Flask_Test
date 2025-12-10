from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/data", methods=["POST"])
def receive_data():
    data = request.get_json()
    print("✅ Received from UNO Q:", data)
    return jsonify({"status": "ok"})

@app.route("/")
def home():
    return "UNO Q Flask Server Running ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Render uses port 10000
