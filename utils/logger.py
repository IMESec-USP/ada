from datetime import datetime
from sys import stdout


class Logger:
    class LoggerWithContext:
        def __init__(self, parent_logger, context):
            self._context = context
            self.parent_logger = parent_logger

        def log(self, message: str):
            self.parent_logger.fpointer.write(f'[{datetime.now()}] [{self._context}] {message}\n')
            self.parent_logger.fpointer.flush()

    def __init__(self, log_file: str):
        self.fpointer = open(log_file, 'a') if log_file else stdout

    def with_class_name(self, obj):
        return self.LoggerWithContext(self, obj.__class__.__name__)
    
    def log(self, message: str):
        self.fpointer.write(f'[{datetime.now()}] {message}\n')
        self.fpointer.flush()