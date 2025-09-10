import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
API_BASE = os.getenv("API_BASE", "https://youtube-download-api-production-4bd1.up.railway.app")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a YouTube link, I'll fetch MP3 for you!")

def get_download_link(url):
    r = requests.get(f"{API_BASE}/mp3", params={"url": url})
    if r.status_code == 200:
        return r.json().get("url")
    return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        await update.message.reply_text("Please send a valid YouTube link 🔗")
        return

    await update.message.reply_text("⏳ Downloading, please wait...")
    try:
        dl_url = get_download_link(url)
        if not dl_url:
            await update.message.reply_text("❌ Failed to get file link.")
            return

        # download file
        resp = requests.get(dl_url, stream=True)
        filename = "temp.mp3"
        with open(filename, "wb") as f:
            for chunk in resp.iter_content(1024 * 1024):
                f.write(chunk)

        # send audio
        with open(filename, "rb") as f:
            await update.message.reply_audio(audio=f, title="Downloaded Song 🎵")

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
