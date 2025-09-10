import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE = "https://youtube-download-api.matheusishiyama.repl.co"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Send me a YouTube link and choose format:\n"
        "🎶 Type /mp3 <url> for audio\n"
        "🎥 Type /mp4 <url> for video"
    )

async def download_mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /mp3 <YouTube URL>")
        return
    
    url = context.args[0]
    try:
        response = requests.get(f"{API_BASE}/mp3", params={"url": url})
        if response.status_code == 200:
            await update.message.reply_document(
                document=response.content,
                filename="song.mp3",
                caption="✅ Downloaded MP3"
            )
        else:
            await update.message.reply_text("❌ Failed to get MP3. Check the link.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

async def download_mp4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /mp4 <YouTube URL>")
        return
    
    url = context.args[0]
    try:
        response = requests.get(f"{API_BASE}/mp4", params={"url": url})
        if response.status_code == 200:
            await update.message.reply_document(
                document=response.content,
                filename="video.mp4",
                caption="✅ Downloaded MP4"
            )
        else:
            await update.message.reply_text("❌ Failed to get MP4. Check the link.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mp3", download_mp3))
    app.add_handler(CommandHandler("mp4", download_mp4))

    app.run_polling()
