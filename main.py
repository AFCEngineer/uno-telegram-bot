import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler
from uno_game import UnoGame

app = Flask(__name__)
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("TOKEN environment variable not set.")

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)
game = UnoGame()

# Command handlers
def start(update: Update, context):
    update.message.reply_text("🎮 Welcome to UNO Bot!\nUse /join to join a game.")

def join(update: Update, context):
    user_id = update.message.from_user.id
    success = game.add_player(user_id)
    if success:
        update.message.reply_text("✅ You joined the game.")
    else:
        update.message.reply_text("❌ Game full or already joined.")

def begin(update: Update, context):
    if game.start_game():
        update.message.reply_text(f"🚀 Game started! Top card: {game.top_card}")
    else:
        update.message.reply_text("❗ Need at least 2 players to start.")

def hand(update: Update, context):
    user_id = update.message.from_user.id
    hand = game.get_hand(user_id)
    update.message.reply_text(f"🃏 Your hand: {', '.join(hand)}")

def play(update: Update, context):
    user_id = update.message.from_user.id
    card = ' '.join(context.args)
    result = game.play_card(user_id, card)
    update.message.reply_text(result)

def draw(update: Update, context):
    user_id = update.message.from_user.id
    result = game.draw_card(user_id)
    update.message.reply_text(result)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("join", join))
dispatcher.add_handler(CommandHandler("begin", begin))
dispatcher.add_handler(CommandHandler("hand", hand))
dispatcher.add_handler(CommandHandler("play", play))
dispatcher.add_handler(CommandHandler("draw", draw))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "UNO Bot is running!"
