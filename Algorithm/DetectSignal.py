from datetime import datetime
from Utils.Redis import redis_manager
from Utils.GlobalConfig import BARS, ALLOW_ONCE_TIME_ORDER
import numpy as np
import pandas as pd
import redis
from Algorithm.HeikenAshi import calculate_heiken_ashi,detect_signal_heiken_ashi
from Algorithm.Prediction.StockModelPrediction import StockModelSelector
def detect_signal(symbol, data):
    # Thiết lập cửa sổ thời gian cho SMA và độ lệch chuẩn
    window = int(BARS)
    # Tính toán SMA cho giá đóng cửa
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data['MA_5'] = data['Close'].rolling(window=5).mean()
    # Tính toán MACD
    # EMA ngắn hạn
    data['short_ema'] = data['Close'].ewm(span=12, adjust=False).mean()
    # EMA dài hạn
    data['long_ema'] = data['Close'].ewm(span=26, adjust=False).mean()
    # Tính MACD
    data['MACD'] = data['short_ema'] - data['long_ema']
    # Tính Signal Line
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

    # features = ['Open', 'High', 'Low', 'Close', 'Volume', 'MA_5']
    # target = 'Target'
    # selector = StockModelSelector()
    # selector.train_and_evaluate(data, features, target)
    # X_new = pd.DataFrame(data)  # Tạo DataFrame mới
    # predictions = selector.predict(X_new)
    #
    # print(predictions)
    #
    # # Convert predictions to DataFrame if they are not already
    # if isinstance(predictions, pd.DataFrame) and len(predictions) == len(data):
    #     data['Target'] = predictions['Target'].values
    # else:
    #     print("Kích thước của dự đoán không khớp với DataFrame data.")
    #
    # print(data)
    # Phần mã tiếp theo giữ nguyên

    ha_df = calculate_heiken_ashi(data)
    ha_signal = detect_signal_heiken_ashi(ha_df)
    # print(ha_data)
    pd.set_option('display.max_columns', None)
    # print(data)
    # Tạo cột tín hiệu mua
    # print( (predictions['Target'] == 1))
    # print(predictions)
    data['Buy_Signal'] = ((ha_signal['Signal'] == 'Buy') &
                          (ha_signal['Trend'] == 'Upward') &
                          (ha_signal['Strength'] == 'Increasing') &
                          (data['MACD'] > data['Signal_Line']) &
                          (data['Close'] > data['SMA']))

    data['Sell_Signal'] = ((ha_signal['Signal'] == 'Sell') &
                           (ha_signal['Trend'] == 'Downward') &
                           (ha_signal['Strength'] == 'Increasing') &
                           (data['MACD'] < data['Signal_Line']) &
                           (data['Close'] < data['SMA']))

    # print(data)

    # ##############################################Step 3: Đẩy dữ liệu qua Redis##############################################
    # Nếu có tín hiệu thì đẩy qua Redis
    # Datetime  Open    High    Low	Close   Volume  SMA short_ema   long_ema    MACD    Signal_Line Buy_Signal  Sell_Signal
    # Tạo kết nối Redis
    # r = redis.Redis(host='localhost', port=6379, db=0)
    # Tạo hash key
    # hash_key = 'OG_FX_MACD,MA'
    last_record = data.iloc[-1]
    # Chuyển đổi record cuối cùng thành từ điển và lưu vào Redis dưới dạng hash
    if (last_record['Buy_Signal'] == True or last_record['Sell_Signal'] == True):
        for field, value in last_record.to_dict().items():
            # Chuyển đổi giá trị uint64 và Timestamp thành chuỗi
            if isinstance(value, pd.Timestamp):
                value = value.isoformat()
            elif isinstance(value, (int, np.uint64)):
                value = str(value)
            SYMBOL_OPENED = symbol+"_IS_OPENED"
            pairsOpened = redis_manager.get_value(SYMBOL_OPENED)
            if ALLOW_ONCE_TIME_ORDER == True and pairsOpened == 'True':
                print(f"Pairs: {symbol} - Đã được mở lệnh")
                return
            else:
                redis_manager.hset_value(symbol, field, value)

            # print(redis_manager.get_value(symbol))
            # r.hset(hash_key, field, value)
            # r.hset(hash_key, 'Symbol', symbol)
            # r.hset(hash_key, 'Insertdate', datetime.now().isoformat())
        # print(last_record)
        print(f"Pairs: {symbol} - Có tín hiệu giao dịch")
    else:
        print(f"Pairs: {symbol} - Không có tín hiệu giao dịch")
