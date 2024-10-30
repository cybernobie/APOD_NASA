from pyrogram import Client, filters
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define your API keys
NASA_API_KEY = os.getenv("NASA_API_KEY")
TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID"))
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# NASA APOD URL
APOD_URL = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"

# Initialize Pyrogram Client
app = Client("apod_bot", bot_token=TELEGRAM_BOT_TOKEN, api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)

def get_apod():
    """Fetch the APOD details from NASA API."""
    response = requests.get(APOD_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return None
@app.on_message(filters.command("start"))
def start(client, message):
    """Send a welcome message when the /start command is used."""
    message.reply_text(
        "Hello! I am the APOD Bot. 🌌\n\n"
        "Use /apod to get NASA's Astronomy Picture of the Day.\n"
        "For more information, use /help."
    )

@app.on_message(filters.command("help"))
def help_command(client, message):
    """Send help information when the /help command is used."""
    message.reply_text(
        "🔹 *APOD Bot Help*\n\n"
        "This bot provides NASA's Astronomy Picture of the Day.\n\n"
        "Available commands:\n"
        "/start - Welcome message\n"
        "/help - Information about commands\n"
        "/apod - Fetch today's APOD from NASA"
    )
@app.on_message(filters.command("apod"))
def send_apod(client, message):
    """Send the APOD image and details to the user."""
    apod_data = get_apod()
    if apod_data:
        title = apod_data['title']
        explanation = apod_data['explanation']
        media_url = apod_data['url']
        copyright = apod_data['copyright']
        # Send APOD media and text to Telegram
        if apod_data["media_type"] == "image":
            client.send_photo(
                chat_id=message.chat.id,
                photo=media_url,
                caption=f"📷 <b>{title}</b>\n\n{explanation}\n\nCopyright:{copyright}\n Credit : nasa.gov"
            )
        elif apod_data["media_type"] == "video":
            client.send_message(
                chat_id=message.chat.id,
                text=f"🎥 {title}\n\n{explanation}\n\nWatch here: {media_url}\n Credit : nasa.gov"
            )
    else:
        message.reply_text("Failed to fetch the APOD. Please try again later.")

if __name__ == "__main__":
    app.run()
