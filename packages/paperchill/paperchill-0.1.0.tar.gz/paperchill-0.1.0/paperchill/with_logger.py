from logging import Logger


class WithLogger:  # pylint: disable = too-few-public-methods
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def info(self, message: str) -> None:
        self.logger.info(message)
