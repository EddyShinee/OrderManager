from datetime import datetime

from Common.Data.LoadDataMT4 import LoadDataFromMT4
from Common.Telegram.SendNotification import send_message
from Common.Utils.GlobalConfig import BASE_API_URL, ORDER_SEND, PIPS, LOTS, TIME_FRAME
from Common.Utils.HttpRequest import make_get_request
from Common.Utils.Redis import redis_manager



def send_order(symbol, data):
    decoded_data = {key.decode('utf-8'): value.decode('utf-8') for key, value in data.items()}
    mt4_data = LoadDataFromMT4()
    token = mt4_data.get_token()
    print("Retrieved token:", token)
    operation = ""
    price = float(decoded_data['Close'])
    pips = 0.0001 * int(PIPS)
    if (decoded_data['Sell_Signal'] == "True") and (decoded_data['Buy_Signal'] == "False"):
        operation = "Sell"
        take_profit = float(price - pips)
        stop_loss = float(price + (pips * 2))
    if (decoded_data['Buy_Signal'] == "True") and (decoded_data['Sell_Signal'] == "False"):
        operation = "Buy"
        take_profit = float(price + pips)
        stop_loss = float(price - (pips * 2))
    params = {
        "id": token,
        "symbol": symbol,
        "operation": operation,
        "volume": LOTS,
        "stoploss": stop_loss,
        "takeprofit": take_profit,
        "comment": f"[Eddy] {symbol} - {operation} - {LOTS} - {round(price, 5)} - {datetime.now()}",
        "placedType": "Signal"
    }
    url = BASE_API_URL + ORDER_SEND
    print("===========================================================")
    print(f"Send Order Success: {params} - Time: {datetime.now()}")
    print("===========================================================")
    remove_data_from_redis(symbol)
    str_message = f"Symbol: {symbol}, Time: {datetime.now()}, Volume: {LOTS}, Type: {operation}, Timeframe: {TIME_FRAME}"
    send_message(str_message)
    return make_get_request(url, params=params)




def remove_data_from_redis(symbol):
    return redis_manager.remove_hset(symbol)