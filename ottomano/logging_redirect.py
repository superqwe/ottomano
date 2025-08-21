import sys


class DualStream:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.console = sys.__stdout__  # output originale

    def write(self, message):
        message = message.strip()
        if message:
            self.logger.log(self.level, message)
            self.console.write(message + '\n')  # stampa anche in console

    def flush(self):
        self.console.flush()
