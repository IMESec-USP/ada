from datetime import datetime
from sys import stdout
class Logger:

    def __init__(self, log_file: str):
        self.fpointer = open(log_file, 'a') if log_file else stdout
    
    def log(self, message: str):
        self.fpointer.write(f'[{datetime.now()}] {message}\n')
        self.fpointer.flush()