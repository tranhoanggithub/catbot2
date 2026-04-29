import os
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from fastapi import FastAPI, Request, Response
from telegram.ext._utils.webhook import run_webhook

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "TOKEN_CUA_BAN")

app_bot = Application.builder().token(TOKEN).build()

async def get_cat_image():
    url = "https://api.thecatapi.com/v1/images/search"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)    
        data = response.json()
        return data[0]['url']

async def meo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Đang tìm mèo...")
    cat_url = await get_cat_image()
    await update.message.reply_photo(cat_url, caption="Meo meo!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Gửi /meo để xem ảnh mèo.")

app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CommandHandler("meo", meo))

fast_app = FastAPI()

@fast_app.post("/webhook")
async def webhook(request: Request):
    req = await request.json()
    update = Update.de_json(req, app_bot.bot)
    await app_bot.process_update(update)
    return Response(status_code=200)
