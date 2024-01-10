import redis


class RedisManager:
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.connection = None

    def connect(self):
        """Kết nối đến Redis server."""
        self.connection = redis.Redis(host=self.host, port=self.port, db=self.db)
        return self.connection

    def set_value(self, key, value):
        """Lưu trữ giá trị trong Redis."""
        if self.connection is None:
            self.connect()
        self.connection.set(key, value)

    def get_value(self, key):
        """Lấy giá trị từ Redis."""
        if self.connection is None:
            self.connect()
        return self.connection.get(key)

    def hset_value(self, name, key, value):
        """Lưu trữ giá trị trong hash của Redis."""
        if self.connection is None:
            self.connect()
        self.connection.hset(name, key, value)

    def hget_value(self, name, key):
        """Lấy giá trị từ hash trong Redis."""
        if self.connection is None:
            self.connect()
        return self.connection.hget(name, key)

    def get_all_set_values(self, set_name):
        """Retrieve all values from a set in Redis."""
        if self.connection is None:
            self.connect()
        return self.connection.hgetall(set_name)

    def remove_hset(self, key):
        if self.connection is None:
            self.connect()
        return self.connection.delete(key)


# Tạo một instance của RedisManager để sử dụng toàn cục
redis_manager = RedisManager()
