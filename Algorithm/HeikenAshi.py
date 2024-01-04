import pandas as pd
# import mplfinance as mpf

def calculate_heiken_ashi(original_df):
    # Check if required fields exist in the DataFrame
    required_fields = ['Open', 'High', 'Low', 'Close']
    if not all(field in original_df for field in required_fields):
        raise ValueError("DataFrame must contain 'Open', 'High', 'Low', 'Close' columns")

    # Copy the original DataFrame to a new DataFrame
    df = original_df.copy()

    df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    ha_open = [(df['Open'][0] + df['Close'][0]) / 2] + [0] * (len(df) - 1)

    for i in range(1, len(df)):
        ha_open[i] = (ha_open[i - 1] + df['HA_Close'].iloc[i - 1]) / 2
    df['HA_Open'] = ha_open
    df['HA_High'] = df[['HA_Open', 'HA_Close', 'High']].max(axis=1)
    df['HA_Low'] = df[['HA_Open', 'HA_Close', 'Low']].min(axis=1)

    return df

def detect_signal_heiken_ashi(heiken_ashi_df):
    # Check if required fields exist in the DataFrame
    required_fields = ['HA_Open', 'HA_High', 'HA_Low', 'HA_Close']
    if not all(field in heiken_ashi_df for field in required_fields):
        raise ValueError("DataFrame must contain 'HA_Open', 'HA_High', 'HA_Low', 'HA_Close' columns")

    # Copy the original DataFrame to a new DataFrame
    df = heiken_ashi_df.copy()

    # Xác định tín hiệu
    df['Signal'] = 'Hold'
    df.loc[df['HA_Close'] > df['HA_Open'], 'Signal'] = 'Buy'
    df.loc[df['HA_Close'] < df['HA_Open'], 'Signal'] = 'Sell'

    # Xác định xu hướng
    df['Trend'] = 'Sideways'
    df.loc[df['HA_Close'] > df['HA_Open'], 'Trend'] = 'Upward'
    df.loc[df['HA_Close'] < df['HA_Open'], 'Trend'] = 'Downward'

    # Đánh giá sức mạnh của xu hướng
    df['Strength'] = 'Stable'
    df.loc[(df['Trend'] == df['Trend'].shift(1)) &
           (df['HA_High'] > df['HA_High'].shift(1)) &
           (df['HA_Low'] < df['HA_Low'].shift(1)), 'Strength'] = 'Increasing'
    df.loc[df['Trend'] != df['Trend'].shift(1), 'Strength'] = 'Changing'

    return df

# Example usage:
# data is a DataFrame containing the columns Open, High, Low, and Close
# heiken_ashi_data = calculate_heiken_ashi(data)
# signals = detect_signal_heiken_ashi(heiken_ashi_data)
