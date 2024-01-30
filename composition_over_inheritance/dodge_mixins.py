"""
FilteredSocketLogger in the multiple inherit needed its own custom __init__()
method because it needed to accept arguments for both of its base classes.

But it turns out that this liability can be avoided. In cases
where a subclass doesn’t require any extra data, the problem doesn’t arise.
"""

import sys
import socket

# Our original example’s base class and subclasses.


class Logger(object):
    def __init__(self, file):
        self.file = file

    def log(self, message):
        self.file.write(message + "\n")
        self.file.flush()


class SocketLogger(Logger):
    def __init__(self, sock):
        self.sock = sock

    def log(self, message):
        self.sock.sendall((message + "\n").encode("ascii"))


# Making this more friendly to multiple ineheritance
class FilteredLogger(Logger):
    pattern = ""

    def log(self, message):
        if self.pattern in message:
            super().log(message)


class FilteredSocketLogger(FilteredLogger, SocketLogger):
    pass  # This subclass needs no extra code!


# The caller can just set “pattern” directly.

print("============= MRO without mixin ============= ")
print(FilteredSocketLogger.__mro__)

sock1, sock2 = socket.socketpair()
logger = FilteredSocketLogger(sock1)
logger.pattern = "Error"


logger.log("Warning: not that important")
logger.log("Error: this is important")

print("The socket received: %r" % sock2.recv(512))
print("\n")


# Making this class mixin by avoiding subclassing
"""
It has no base class that might complicate method resolution order,
so super() will always call the next base class listed in the class statement.
"""


class FilterMixin:
    pattern = ""

    def log(self, message):
        if self.pattern in message:
            super().log(message)


class FileLogger:
    def __init__(self, file):
        self.file = file

    def log(self, message):
        self.file.write(message + "\n")
        self.file.flush()


class FilteredLogger(FilterMixin, FileLogger):
    pass


print("========= MRO with mixin ==========")
print(FilteredLogger.__mro__)
logger = FilteredLogger(sys.stdout)
logger.pattern = "Error"
logger.log("Warning: not that important")
logger.log("Error: this is important")
