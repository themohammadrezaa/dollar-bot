# -------------------------------------------------------------
# ربات تلگرام قیمت دلار و طلا
# این فایل سه کار می‌کنه:
#   ۱) وقتی کسی به ربات دستور /price بده، قیمت لحظه‌ای رو جواب می‌ده
#   ۲) هر ۱۰ دقیقه (قابل تنظیم) خودکار قیمت رو تو کانال می‌فرسته
#   ۳) قیمت‌ها رو با وب‌اسکرپینگ از سایت tgju.org می‌گیره (نه API)
# -------------------------------------------------------------

import os
import time
import threading
import logging

import requests
from bs4 import BeautifulSoup
import telebot

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("price-bot")

# این متغیرها از تنظیمات Railway (Variables) خونده می‌شن، نه از تو کد
BOT_TOKEN = os.environ["BOT_TOKEN"]            # توکنی که از BotFather گرفتی
CHANNEL_ID = os.environ["CHANNEL_ID"]          # مثلا: @Bat_dollar یا -1001234567890
INTERVAL_SECONDS = int(os.environ.get("INTERVAL_SECONDS", "600"))  # فاصله ارسال به کانال (ثانیه)، پیش‌فرض ۶۰۰ = ۱۰ دقیقه

bot = telebot.TeleBot(BOT_TOKEN)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}

SOURCE_URL = "https://www.tgju.org/"


def get_prices():
    """
    این تابع صفحه‌ی اصلی tgju.org رو دانلود می‌کنه و از توش
    قیمت دلار و طلای ۱۸ عیار رو پیدا می‌کنه (وب‌اسکرپینگ، نه API).
    اگه یه روز ساختار سایت عوض شد و قیمت‌ها "نامشخص" برگشت،
    فقط کافیه همین تابع رو اصلاح کنی؛ بقیه‌ی کد دست نمی‌خوره.
    """
    resp = requests.get(SOURCE_URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    def get_price_by_id(row_id):
        row = soup.find("tr", {"data-market-row": row_id}) or soup.find("li", id=row_id)
        if not row:
            return None
        val = row.find(class_="info-price") or row.find("td")
        return val.get_text(strip=True) if val else None

    dollar = get_price_by_id("price_dollar_rl")
    gold18 = get_price_by_id("geram18")

    return {
        "dollar": dollar or "نامشخص",
        "gold18": gold18 or "نامشخص",
    }


def format_message(prices):
    return (
        "💵 قیمت لحظه‌ای\n\n"
        f"دلار: {prices['dollar']} ریال\n"
        f"طلای ۱۸ عیار: {prices['gold18']} تومان\n"
    )


@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    bot.reply_to(message, "دستور /price رو بزن تا قیمت لحظه‌ای دلار و طلا رو بگیری.")


@bot.message_handler(commands=["price"])
def cmd_price(message):
    try:
        prices = get_prices()
        bot.reply_to(message, format_message(prices))
    except Exception as e:
        log.exception("error fetching prices")
        bot.reply_to(message, f"خطا در دریافت قیمت: {e}")


def channel_broadcaster():
    while True:
        try:
            prices = get_prices()
            bot.send_message(CHANNEL_ID, format_message(prices))
            log.info("sent prices to channel")
        except Exception:
            log.exception("error broadcasting to channel")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    t = threading.Thread(target=channel_broadcaster, daemon=True)
    t.start()
    log.info("bot polling started")
    bot.infinity_polling()
