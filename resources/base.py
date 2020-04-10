class BaseResource:

    def __init__(self, logger, telegram_broadcaster):
        self.logger = logger
        self.broadcaster = telegram_broadcaster
        self.has_json_body = False

    def log(self, message=''):
        name = self.__class__.__name__
        self.logger.log(f'{name}: {message}')

    