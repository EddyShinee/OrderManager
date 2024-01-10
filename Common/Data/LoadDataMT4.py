from datetime import datetime

import pandas as pd

from Algorithm.DetectSignal import detect_signal
from Common.Utils.GlobalConfig import BASE_API_URL, USER, PASSWORD, HOST, PORT, TIME_FRAME, BARS, API_CONNECT, SYMBOLS, \
    API_HISTORY_PRICE_MANY
from Common.Utils.HttpRequest import make_get_request


class LoadDataFromMT4:
    def __init__(self):
        self.base_url = BASE_API_URL
        self.path_connect = API_CONNECT
        self.account_number = USER
        self.password = PASSWORD
        self.host = HOST
        self.port = PORT
        self.api_get_symbols = API_HISTORY_PRICE_MANY
        self.symbols = SYMBOLS

    def get_token(self):
        print("Get account token")
        url = self.base_url + self.path_connect
        request_params = {
            'user': self.account_number,
            'password': self.password,
            'host': self.host,
            'port': self.port
        }
        return make_get_request(url, params=request_params)

    def load_data_mt4(self):
        token = self.get_token()
        print("Token: " + token)
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%dT%H:%M:%S")
        url = self.base_url + self.api_get_symbols
        request_params = {
            "id": token,
            "symbol": self.symbols,
            "timeframe": TIME_FRAME,
            "from": formatted_now,
            "count": BARS
        }
        print(f"Get data pairs: {self.symbols} - Time: {now}")
        return make_get_request(url, params=request_params)

    @staticmethod
    def process_data(currency_pair):
        symbol = currency_pair['symbol']
        # print(f"Symbol: {symbol}")
        bars = currency_pair['bars']
        data = pd.DataFrame(bars)
        data['time'] = pd.to_datetime(data['time'])
        data = data.rename(columns={'time': 'Datetime'})
        data = data.rename(columns={'open': 'Open'})
        data = data.rename(columns={'high': 'High'})
        data = data.rename(columns={'low': 'Low'})
        data = data.rename(columns={'close': 'Close'})
        data = data.rename(columns={'volume': 'Volume'})
        data = pd.DataFrame(data, columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])
        return data

    def run(self):
        response_data = self.load_data_mt4()
        if response_data is None:
            print("System Error")
            return
        for currency_pair in response_data:
            symbol = currency_pair['symbol']
            data = self.process_data(currency_pair)
            detect_signal(symbol, data)
            # Xử lý code data ở đây
            # Hãy xử ly1 thêm code ở chỗ naày
            # print(data)
