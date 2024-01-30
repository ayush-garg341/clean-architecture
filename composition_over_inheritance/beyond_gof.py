"""
Python’s logging module wanted even more flexibility:
- not only to support multiple filters
- but to support multiple outputs for a single stream of log messages.

To know more about this, read about configuring loggers in django.

"""

import sys
import syslog


class Logger:
    def __init__(self, filters, handlers):
        self.filters = filters
        self.handlers = handlers

    def log(self, msg):
        if all(f.match(msg) for f in self.filters):
            for h in self.handlers:
                h.emit(msg)


# Filters now know only about strings!

"""
All of the previous designs either hid filtering inside one of the logging
classes itself, or saddled filters with additional duties beyond simply
rendering a verdict.

Finally decoupled from the specific concept of logging, it will be easier
to test and maintain.
"""


class TextFilter:
    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, text):
        return self.pattern in text


# Handlers look like “loggers” did in the previous solution.


class FileHandler:
    def __init__(self, file):
        self.file = file

    def emit(self, message):
        self.file.write(message + "\n")
        self.file.flush()


class SocketHandler:
    def __init__(self, sock):
        self.sock = sock

    def emit(self, message):
        self.sock.sendall((message + "\n").encode("ascii"))


class SyslogHandler:
    def __init__(self, priority):
        self.priority = priority

    def emit(self, message):
        syslog.syslog(self.priority, message)


"""
Design principles like Composition Over Inheritance are, in the end,
more important than individual patterns like the Adapter or Decorator.
"""

if __name__ == "__main__":
    f = TextFilter("Error")
    h = FileHandler(sys.stdout)
    logger = Logger([f], [h])

    logger.log("Ignored: this will not be logged")
    logger.log("Error: this is important")
