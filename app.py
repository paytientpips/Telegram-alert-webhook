from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400

    text = f"📣 Alert: {data.get('event','')}\\nSymbol: {data.get('symbol','')}\\nPrice: {data.get('price','')}\\nTime: {data.get('time','')}"
    response = requests.post(TELEGRAM_URL, json={"chat_id": CHAT_ID, "text": text})

    if response.status_code != 200:
        return jsonify({"error": "Failed to send to Telegram"}), 500

    return jsonify({"status": "sent"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
