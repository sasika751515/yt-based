import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
API_BASE = "https://youtube-download-api-production-4bd1.up.railway.app"

def start(update, context):
    update.message.reply_text("👋 Send me a YouTube link, I'll fetch MP3 for you!")

def get_download_link(url):
    """Call external API and return direct download link"""
    r = requests.get(f"{API_BASE}/mp3", params={"url": url})
    if r.status_code == 200:
        return r.json().get("url")
    return None

def handle_message(update, context):
    url = update.message.text.strip()
    if not url.startswith("http"):
        update.message.reply_text("Please send a valid YouTube link 🔗")
        return

    update.message.reply_text("⏳ Downloading, please wait...")
    try:
        dl_url = get_download_link(url)
        if not dl_url:
            update.message.reply_text("❌ Failed to get file link.")
            return

        # download file to temp.mp3
        resp = requests.get(dl_url, stream=True)
        filename = "temp.mp3"
        with open(filename, "wb") as f:
            for chunk in resp.iter_content(1024 * 1024):
                f.write(chunk)

        # send audio file
        with open(filename, "rb") as f:
            update.message.reply_audio(audio=f, title="Downloaded Song 🎵")

        # cleanup
        os.remove(filename)

    except Exception as e:
        update.message.reply_text(f"⚠️ Error: {e}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
