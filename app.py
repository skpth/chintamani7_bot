from flask import Flask, request
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "Chintamani7 Bot is live"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received update:", data)
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)# Flask + Telegram bot logic
