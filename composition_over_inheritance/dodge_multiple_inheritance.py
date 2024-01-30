"""
Some Python projects fall short of practicing Composition Over Inheritance
because they are tempted to dodge the principle by means of a controversial
feature of the Python language: multiple inheritance.
"""
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


class FilteredLogger(Logger):
    def __init__(self, pattern, file):
        self.pattern = pattern
        super().__init__(file)

    def log(self, message):
        if self.pattern in message:
            super().log(message)


# A class derived through multiple inheritance.


class FilteredSocketLogger(FilteredLogger, SocketLogger):
    def __init__(self, pattern, sock):
        FilteredLogger.__init__(self, pattern, None)
        SocketLogger.__init__(self, sock)


print(FilteredSocketLogger.__mro__)
sock1, sock2 = socket.socketpair()
logger = FilteredSocketLogger("Error", sock1)
logger.log("Warning: not that important")
logger.log("Error: this is important")

print("The socket received: %r" % sock2.recv(512))
