from flask import Flask, request
import telebot
import json
import os
from model.predictor import predict_next

TOKEN = '7797596863:AAHETWZXRdf5BcTKizXXM8Jn4CYwi_et8dI'  # Bot token already set
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

DB_FILE = 'outcomes.json'

if not os.path.exists(DB_FILE):
    with open(DB_FILE, 'w') as f:
        json.dump([], f)

# Helper Functions
def load_outcomes():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_outcomes(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f)

# Routes
@app.route(f'/{TOKEN}', methods=['POST'])
def telegram_webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return 'ok'

# Bot Handlers
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to Chintamani7 AI Bot! Send outcomes or use /train /predict.")

@bot.message_handler(commands=['train'])
def train(message):
    outcomes = load_outcomes()
    bot.send_message(message.chat.id, f"Training completed on {len(outcomes)} outcomes!")

@bot.message_handler(commands=['predict'])
def predict(message):
    outcomes = load_outcomes()
    if len(outcomes) < 5:
        bot.send_message(message.chat.id, "Need at least 5 outcomes to predict!")
        return
    prediction = predict_next(outcomes[-5:])
    bot.send_message(message.chat.id, f"Next Prediction: {prediction}")

@bot.message_handler(func=lambda m: True)
def add_outcome(message):
    text = message.text.strip().upper()
    if text in ['B', 'S']:
        outcomes = load_outcomes()
        outcomes.append(text)
        if len(outcomes) > 500000:
            outcomes.pop(0)
        save_outcomes(outcomes)
        bot.send_message(message.chat.id, f"Added {text}. Total entries: {len(outcomes)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
