class BaseResource:

    def __init__(self, logger, telegram_broadcaster):
        self.logger = logger.with_class_name(self)
        self.broadcaster = telegram_broadcaster
        self.has_json_body = False
