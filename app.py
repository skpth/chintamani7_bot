from flask import Flask, request
import os
import json
import requests

app = Flask(__name__)

BOT_TOKEN = '7797596863:AAHETWZXRdf5BcTKizXXM8Jn4CYwi_et8dI'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route('/')
def home():
    return "Chintamani7 Bot is live"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        message_text = data["message"].get("text", "")

        if message_text == "/start":
            send_message(chat_id, "Welcome to Chintamani7 Prediction Bot!")
        elif message_text == "/status":
            send_message(chat_id, "Bot is running and ready.")
        else:
            send_message(chat_id, f"You said: {message_text}")

    return "OK", 200

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    headers = {"Content-Type": "application/json"}
    requests.post(url, json=payload, headers=headers)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
