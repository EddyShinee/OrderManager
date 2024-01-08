import configparser
import os


class GlobalConfig:
    def __init__(self, config_file='Common/Config/config.ini'):
        self.config = configparser.ConfigParser()
        self.load_config(config_file)

    def load_config(self, config_file):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"The config file {config_file} does not exist.")
        self.config.read(config_file)

    def get_api_domain(self, env):
        return self.config.get(env, 'base_api_url', fallback=None)

    def get_api_connect(self):
        return self.config.get('api_account', 'connect', fallback=None)

    def get_log_path(self):
        return self.config.get('DEFAULT', 'log_path', fallback=None)

    def get_ping(self):
        return self.config.get('api_service', 'ping', fallback=None)

    def get_user(self):
        return self.config.get(environment, 'account_number', fallback=None)

    def get_password(self):
        return self.config.get(environment, 'password', fallback=None)

    def get_host(self):
        return self.config.get(environment, 'host', fallback=None)

    def get_port(self):
        return self.config.get(environment, 'port', fallback=None)

    def get_telegram_token(self):
        return self.config.get('telegram', 'token', fallback=None)

    def get_telegram_chat_id(self):
        return self.config.get('telegram', 'chat_id', fallback=None)

    def get_telegram_domain(self):
        return self.config.get('telegram', 'domain', fallback=None)

    def get_telegram_send_message(self):
        return self.config.get('telegram', 'send_message', fallback=None)

    def get_list_symbols(self):
        return self.config.get('DEFAULT', 'symbols', fallback=None)

    def get_api_history_price_many(self):
        return self.config.get('api_quote_history', 'price_history_many', fallback=None)

    def get_time_frame(self):
        return self.config.get('api_quote_history', 'time_frame', fallback=None)

    def get_count_bar(self):
        return self.config.get('api_quote_history', 'count_bars', fallback=None)

    def get_once_time_order(self):
        return self.config.get('DEFAULT', 'once_time_order', fallback=True)

    def get_order_send(self):
        return self.config.get('api_orders','order_send', fallback=True )

    def get_pips(self):
        return self.config.get('order_config', 'pips', fallback=None)

    def get_lots(self):
        return self.config.get('order_config', 'lots', fallback=None)

# Sử dụng GlobalConfig
try:
    config = GlobalConfig()
    environment = os.getenv('APP_ENV', 'production')
    BASE_API_URL = config.get_api_domain(environment)

    LOG_PATH = config.get_log_path()
    API_PING = config.get_ping()

    #Connect
    API_CONNECT = config.get_api_connect()
    USER = config.get_user()
    PASSWORD = config.get_password()
    HOST = config.get_host()
    PORT = config.get_port()

    # Symbols
    SYMBOLS = config.get_list_symbols().split(",")
    API_HISTORY_PRICE_MANY = config.get_api_history_price_many()
    TIME_FRAME = config.get_time_frame()
    BARS = config.get_count_bar()


    # Telegram
    TELEGRAM_TOKEN = config.get_telegram_token()
    TELEGRAM_CHAT_ID = config.get_telegram_chat_id()
    TELEGRAM_DOMAIN = config.get_telegram_domain()
    TELEGRAM_SEND_MESSAGE = config.get_telegram_send_message()

    # Order
    ALLOW_ONCE_TIME_ORDER = config.get_once_time_order()
    ORDER_SEND = config.get_order_send()
    PIPS = config.get_pips()
    LOTS = config.get_lots()

    if not BASE_API_URL or not LOG_PATH:
        raise ValueError("Essential configuration data is missing.")

except Exception as e:
    # Xử lý ngoại lệ tại đây
    print(f"Error loading configuration: {e}")
    # Có thể thêm logging hoặc các biện pháp xử lý lỗi khác tại đây
