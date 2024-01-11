import logging
from datetime import datetime

import time

from Common.Utils.GlobalConfig import SYMBOLS
from Common.Utils.Redis import redis_manager
from Order.Order import send_order

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
                send_order(symbol, data_symbol)
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


if __name__ == "__main__":
    print("Order server is running....")
    main()
