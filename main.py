import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GRADIO_URL = "https://yourname--yourbot.hf.space"

def get_bot_reply(user_input):
    try:
        response = requests.post(f"{GRADIO_URL}/run/predict", json={
            "data": [user_input]
        })
        return response.json()["data"][0]
    except:
        return "Bot error. Try again later."

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    user_input = data["message"]["text"]

    reply = get_bot_reply(user_input)

    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={
        "chat_id": chat_id,
        "text": reply
    })
    return "", 200

@app.route("/", methods=["GET"])
def index():
    return "Bot is running."
