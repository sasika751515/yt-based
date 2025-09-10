import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE = "https://youtube-download-api.matheusishiyama.repl.co"

def start(update, context):
    update.message.reply_text(
        "👋 Hello! Send me a YouTube link and choose format:\n"
        "🎶 Type /mp3 <url> for audio\n"
        "🎥 Type /mp4 <url> for video"
    )

def download_mp3(update, context):
    if not context.args:
        return update.message.reply_text("⚠️ Usage: /mp3 <YouTube URL>")
    
    url = context.args[0]
    try:
        response = requests.get(f"{API_BASE}/mp3", params={"url": url}, stream=True)

        if response.status_code == 200:
            update.message.reply_audio(
                audio=response.content,
                filename="song.mp3",
                title="Downloaded MP3"
            )
        else:
            update.message.reply_text("❌ Failed to get MP3. Please check the link.")
    except Exception as e:
        update.message.reply_text(f"⚠️ Error: {str(e)}")

def download_mp4(update, context):
    if not context.args:
        return update.message.reply_text("⚠️ Usage: /mp4 <YouTube URL>")
    
    url = context.args[0]
    try:
        response = requests.get(f"{API_BASE}/mp4", params={"url": url}, stream=True)

        if response.status_code == 200:
            update.message.reply_video(
                video=response.content,
                filename="video.mp4",
                supports_streaming=True
            )
        else:
            update.message.reply_text("❌ Failed to get MP4. Please check the link.")
    except Exception as e:
        update.message.reply_text(f"⚠️ Error: {str(e)}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("mp3", download_mp3))
    dp.add_handler(CommandHandler("mp4", download_mp4))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
