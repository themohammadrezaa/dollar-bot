import os
import time
import threading
import logging

import requests
from bs4 import BeautifulSoup
import telebot

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("price-bot")

BOT_TOKEN = os.environ["BOT_TOKEN"]           
CHANNEL_ID = os.environ["CHANNEL_ID"]          
INTERVAL_SECONDS = int(os.environ.get("INTERVAL_SECONDS", "600"))  
CHECK_INTERVAL_SECONDS = int(os.environ.get("CHECK_INTERVAL_SECONDS", "120"))

bot = telebot.TeleBot(BOT_TOKEN)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}

SOURCE_URL = "https://www.tgju.org/"
CHANGE_sent = 1
last_sent = {"dollar": None, "gold18": None}

def to_number(price_str):
    try:
        return float(price_str.replace(",", ""))
    except (ValueError, AttributeError):
        return None


def significant_change(old, new):
    if old is None or new is None:
        return True
    if old == 0:
        return True
    return abs(new - old) / old * 100 >= CHANGE_THRESHOLD

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
        f"طلای ۱۸ عیار: {prices['gold18']} ریال\n"
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
            dollar_num = to_number(prices["dollar"])
            gold_num = to_number(prices["gold18"])

            changed = (
                significant_change(last_sent["dollar"], dollar_num)
                or significant_change(last_sent["gold18"], gold_num)
            )

            if changed:
                bot.send_message(CHANNEL_ID, format_message(prices))
                last_sent["dollar"] = dollar_num
                last_sent["gold18"] = gold_num
                log.info("sent prices to channel (change detected)")
            else:
                log.info("no significant change, skipped")
        except Exception:
            log.exception("error broadcasting to channel")
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    t = threading.Thread(target=channel_broadcaster, daemon=True)
    t.start()
    log.info("bot polling started")
    bot.infinity_polling()
