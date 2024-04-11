import logging
import datetime
import os


class Logger:

    def __init__(self, name):

        self.logger = None
        self.log_level = logging.INFO
        self.file_level = logging.DEBUG
        self.log_path = self.get_log_path(name)
        self.stream_level = logging.WARNING
        self.format = logging.Formatter('%(asctime)s [%(module)s.%(funcName)s:%(lineno)d] [%(levelname)s] : %(message)s')
        self.date_format = "%Y-%m-%d %H:%M:%S"

        self.initialize(name)

    def initialize(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.log_level)

        file_handler = logging.FileHandler(self.log_path)
        file_handler.setLevel(self.file_level)
        file_handler.setFormatter(self.format)
        self.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.stream_level)
        stream_handler.setFormatter(self.format)
        self.logger.addHandler(stream_handler)

    def get_log_path(self, name):
        os.makedirs("logs", exist_ok=True)
        os.makedirs(f"logs/{name}", exist_ok=True)

        today = datetime.date.today().strftime("%Y%m%d")

        return f"logs/{name}/{today}.{name}.log"

    def get_logger(self) -> logging.Logger:
        return self.logger
