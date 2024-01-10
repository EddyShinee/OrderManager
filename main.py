import logging
import time
from datetime import datetime

from Common.Data.LoadDataMT4 import LoadDataFromMT4
from Common.Telegram.SendNotification import send_message
from Common.Utils.GlobalConfig import SYMBOLS, BASE_API_URL, ORDER_SEND, PIPS, LOTS
from Common.Utils.HttpRequest import make_get_request
from Common.Utils.Redis import redis_manager

run_seconds = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52,
               54, 56, 58]


def fetch_data_from_redis(symbol):
    data_symbol = redis_manager.get_all_set_values(symbol)
    return data_symbol


def remove_data_from_redis(symbol):
    return redis_manager.remove_hset(symbol)


def schedule_running():
    while True:
        current_time = datetime.now()
        current_second = current_time.second
        symbols = SYMBOLS
        print(f"Fetch data redis: {symbols} - Time: {datetime.now()}")
        # Redis fetching function called every 2 seconds
        for symbol in symbols:
            data_symbol = fetch_data_from_redis(symbol)
            if data_symbol:
                sendOrder(symbol, data_symbol)
            # else:
            #     return None
            # print(f"No data found for symbol: {symbol}")
        # Check if the current minute is in the run_minutes list
        if current_second in run_seconds:
            # Check if the function for the current minute has been run
            last_run = getattr(schedule_running, 'last_run', None)
            if last_run is None or last_run != current_second:
                # code gì
                setattr(schedule_running, 'last_run', current_second)

        # Sleep for 2 seconds before the next loop iteration
        time.sleep(1)


def main():
    try:
        schedule_running()
    except Exception as e:
        logging.error(f'Error during application initialization: {str(e)}')
        raise


def sendOrder(symbol, data):
    decoded_data = {key.decode('utf-8'): value.decode('utf-8') for key, value in data.items()}
    print(type(decoded_data['Sell_Signal']))
    mt4_data = LoadDataFromMT4()
    token = mt4_data.get_token()
    print("Retrieved token:", token)
    operation = ""
    price = float(decoded_data['Close'])
    pips = 0.0001 * int(PIPS)
    if (decoded_data['Sell_Signal'] == "True") and (decoded_data['Buy_Signal'] == "False"):
        operation = "Sell"
        take_profit = float(price - pips)
        stop_loss = float(price + pips)
    if (decoded_data['Buy_Signal'] == "True") and (decoded_data['Sell_Signal'] == "False"):
        operation = "Buy"
        take_profit = float(price + pips)
        stop_loss = float(price - pips)
    params = {
        "id": token,
        "symbol": symbol,
        "operation": operation,
        "volume": LOTS,
        "stoploss": stop_loss,
        "takeprofit": take_profit,
        "comment": {operation},
        "placedType": "Signal"
    }
    url = BASE_API_URL + ORDER_SEND
    print(f"Đặt lệnh thành công {params} - Time: {datetime.now()}")
    remove_data_from_redis(symbol)
    str_message = f"Symbol: {symbol}, Time: {datetime.now()}, Volume: {LOTS}, Type: {operation}"
    send_message(str_message)
    return make_get_request(url, params=params)


if __name__ == "__main__":
    print("Order server is running....")
    main()
