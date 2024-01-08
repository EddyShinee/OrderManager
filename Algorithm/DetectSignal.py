import numpy as np
import pandas as pd

from Algorithm.HeikenAshi import calculate_and_detect_ha_signal
from Algorithm.MACD import calculate_and_detect_macd_signal
from Common.Utils.GlobalConfig import BARS, ALLOW_ONCE_TIME_ORDER
from Common.Utils.Redis import redis_manager


def detect_signal(symbol, data):
    macd_signal = calculate_and_detect_macd_signal(data)
    ha_signal = calculate_and_detect_ha_signal(data)
    pd.set_option('display.max_columns', None)

    data['Buy_Signal'] = ((ha_signal['Signal'] == 'Buy') &
                          (ha_signal['Trend'] == 'Upward') &
                          (ha_signal['Strength'] == 'Increasing') &
                          (macd_signal['MACD'] > macd_signal['Signal_Line']) &
                          (macd_signal['Close'] > macd_signal['SMA']))

    data['Sell_Signal'] = ((ha_signal['Signal'] == 'Sell') &
                           (ha_signal['Trend'] == 'Downward') &
                           (ha_signal['Strength'] == 'Increasing') &
                           (macd_signal['MACD'] < macd_signal['Signal_Line']) &
                           (macd_signal['Close'] < macd_signal['SMA']))

    last_record = data.iloc[-1]
    if (last_record['Buy_Signal'] == True or last_record['Sell_Signal'] == True):
        for field, value in last_record.to_dict().items():
            # Chuyển đổi giá trị uint64 và Timestamp thành chuỗi
            if isinstance(value, pd.Timestamp):
                value = value.isoformat()
            elif isinstance(value, (int, np.uint64)):
                value = str(value)
            SYMBOL_OPENED = symbol + "_IS_OPENED"
            pairsOpened = redis_manager.get_value(SYMBOL_OPENED)
            if ALLOW_ONCE_TIME_ORDER == True and pairsOpened == 'True':
                print(f"Pairs: {symbol} - Opened Order")
                return
            else:
                redis_manager.hset_value(symbol, field, value)
        print(f"Pairs: {symbol} - Trading Signal")
    else:
        print(f"Pairs: {symbol} - No signal")
