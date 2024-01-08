from Common.Utils.GlobalConfig import BARS

def calculate_macd(original_df):
    if not all(field in original_df.columns for field in ['Close']):
        raise ValueError("DataFrame must contain 'Close' column")

    df = original_df.copy()
    window = int(BARS)

    df['SMA'] = df['Close'].rolling(window=window).mean()
    df['MA_5'] = df['Close'].rolling(window=7).mean()
    # Calculate Short-term Exponential Moving Average (EMA)
    df['short_ema'] = df['Close'].ewm(span=12, adjust=False).mean()
    # Calculate Long-term EMA
    df['long_ema'] = df['Close'].ewm(span=26, adjust=False).mean()
    # Calculate MACD
    df['MACD'] = df['short_ema'] - df['long_ema']
    # Calculate Signal Line
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df


def detect_macd(df):
    # Implement your logic to detect signals
    # For example, let's just mark 'Buy' when MACD crosses above Signal Line
    df['Signal'] = 'Hold'
    df.loc[df['MACD'] > df['Signal_Line'], 'Signal'] = 'Buy'
    df.loc[df['MACD'] < df['Signal_Line'], 'Signal'] = 'Sell'
    return df


def calculate_and_detect_macd_signal(original_df):
    # Calculate MACD values
    macd_df = calculate_macd(original_df)
    # Detect signals based on MACD analysis
    final_df = detect_macd(macd_df)
    return final_df
