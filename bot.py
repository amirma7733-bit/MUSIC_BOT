import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 🎵 اسم آهنگ رو بفرست تا برات پیدا کنم.")

async def search_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    await update.message.reply_text(f"🔍 در حال جستجو برای: {query}")

    search_url = f"https://nava-song.com/?s={query.replace(' ', '+')}"
    res = requests.get(search_url)
    soup = BeautifulSoup(res.text, "html.parser")

    mp3_link = None
    for a in soup.find_all("a", href=True):
        if a["href"].endswith(".mp3"):
            mp3_link = a["href"]
            break

    if not mp3_link:
        await update.message.reply_text("❌ آهنگی پیدا نشد.")
        return

    file_data = requests.get(mp3_link)
    file_name = "song.mp3"
    with open(file_name, "wb") as f:
        f.write(file_data.content)

    await update.message.reply_audio(audio=open(file_name, "rb"), title=query)
    os.remove(file_name)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_song))
app.run_polling()  
