from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pytube import YouTube
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /mp3 <YouTube URL>")
        return

    url = context.args[0]
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        file_path = stream.download()
        base, ext = os.path.splitext(file_path)
        new_file = base + ".mp3"
        os.rename(file_path, new_file)

        await update.message.reply_document(
            document=open(new_file, "rb"),
            filename=yt.title + ".mp3",
            caption="✅ MP3 Downloaded"
        )
        os.remove(new_file)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def mp4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /mp4 <YouTube URL>")
        return

    url = context.args[0]
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        file_path = stream.download()

        await update.message.reply_document(
            document=open(file_path, "rb"),
            filename=yt.title + ".mp4",
            caption="✅ MP4 Downloaded"
        )
        os.remove(file_path)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("mp3", mp3))
    app.add_handler(CommandHandler("mp4", mp4))
    app.run_polling()
