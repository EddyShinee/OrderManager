import telegram

from Common.Utils.GlobalConfig import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_message(message):
    try:
        telegram_notify = telegram.Bot(TELEGRAM_TOKEN)
        telegram_notify.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
        print("[Success] Send message to Telegram")
        print("Message: \n" + message)
    except Exception as ex:
        print("[Fail] Send message to Telegram")
        print(ex)
