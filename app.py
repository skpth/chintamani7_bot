from flask import Flask, request
import telegram
import os
from model.predictor import predict_next
from model.train import train_model
from model.backup import backup_outcomes
import json

TOKEN = '7797596863:AAHETWZXRdf5BcTKizXXM8Jn4CYwi_et8dI'
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

# Load previous outcomes
if os.path.exists('outcomes.json'):
    with open('outcomes.json', 'r') as f:
        outcomes = json.load(f)
else:
    outcomes = []

# Training Status
is_training = False

@app.route(f'/{TOKEN}', methods=['POST'])
def telegram_webhook():
    global outcomes
    global is_training

    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message:
        text = update.message.text.lower()
        chat_id = update.message.chat.id

        if text.startswith('/start'):
            bot.sendMessage(chat_id=chat_id, text="Bot started. Send outcomes (B/S) to train or use /predict.")

        elif text.startswith('/predict'):
            if len(outcomes) < 5:
                bot.sendMessage(chat_id=chat_id, text="Not enough data. Please provide at least 5 outcomes.")
            else:
                last_five = outcomes[-5:]
                prediction, confidence = predict_next(last_five)
                bot.sendMessage(chat_id=chat_id, text=f"Prediction: {prediction} with confidence {confidence}%")

        elif text.startswith('/train'):
            train_model(outcomes)
            bot.sendMessage(chat_id=chat_id, text="Model retrained.")

        elif text.startswith('/status'):
            bot.sendMessage(chat_id=chat_id, text=f"Stored outcomes: {len(outcomes)}")

        elif text.startswith('/help'):
            bot.sendMessage(chat_id=chat_id, text="/start /status /predict /train /help")

        else:
            # Accept manual entries B/S
            for c in text:
                if c in ['b', 's']:
                    outcomes.append(c.upper())
            with open('outcomes.json', 'w') as f:
                json.dump(outcomes, f)
            bot.sendMessage(chat_id=chat_id, text=f"Received and saved {len(text)} outcomes.")

    return 'ok'

@app.route('/')
def index():
    return 'Bot is running.'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 10000)))
