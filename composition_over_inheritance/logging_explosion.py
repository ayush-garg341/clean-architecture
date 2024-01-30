"""
We will create a base logger class and then inherit from that to
support various special functionality like filter, storage.
"""

import sys
import syslog
import socket


# Initial Class
class Logger(object):
    def __init__(self, file):
        self.file = file

    def log(self, msg):
        self.file.write(msg + "\n")
        self.file.flush()  # Leaves the file open for more writing
        # By default Python buffers our output and writes it to the file in large chunks.
        # This is faster than writing smaller amounts more often, but it means our
        # output might not actually appear in the file until we close it or Python flushes the buffers.


# Two more classes that sends message elsewhere.
class SocketLogger(Logger):
    def __init__(self, sock):
        self.sock = sock

    def log(self, msg):
        self.sock.sendall((msg + "\n").encode("ascii"))


class SysLogger(Logger):
    def __init__(self, priority):
        self.priority = priority

    def log(self, msg):
        syslog.syslog(self.priority, msg)


"""
The problem arises when this first axis of design is joined by another.
Let's imagine that log messages now needs to be filtered.
EX:- some users only want to see messages with the word “Error” in them.
"""


class FilteredLogger(Logger):
    def __init__(self, pattern, file):
        self.pattern = pattern
        super().__init__(file)

    def log(self, msg):
        if self.pattern in msg:
            super().log(msg)


def filteredLogger():
    f = FilteredLogger("Error", sys.stdout)
    f.log("Ignored: this is not important")
    f.log("Error: but you want to see this")


"""
The trap now has been laid and will be sprung the moment the application
needs to filter messages but write them to a socket instead of a file.
None of the existing classes covers that case.

If developer subclassing and creates a FilteredSocketLogger that combines
the features of both classes, then the subclass explosion is underway.
But in general, case the application will wind up with 3×2=6 classes.

Logger            FilteredLogger
SocketLogger      FilteredSocketLogger
SyslogLogger      FilteredSyslogLogger

The soln is to recognize that a class responsible for both filtering msgs and
logging msgs is too complicated and violating the SRP of SOLID.
"""

"""
SOLUTION NO 1:- ADAPTER PATTERN
1. We keep the original Logger class.
2. We also keep FilteredLogger class.
3. But instead of creating destination-specific subclasses, we adapt each
destination to the behavior of a file and then pass the adapter to a
Logger as its output file.
"""


class FileLikeSocket:
    def __init__(self, sock):
        self.sock = sock

    def write(self, message_and_newline):
        self.sock.sendall(message_and_newline.encode("ascii"))

    def flush(self):
        pass


class SyslogLikeSocket:
    def __init__(self, priority):
        self.priority = priority

    def write(self, message_and_newline):
        message = message_and_newline.rstrip("\n")
        syslog.syslog(self.priority, message)

    def flush(self):
        pass


def filteredSocketLoggerUsingAdapterPattern():
    sock1, sock2 = socket.socketpair()
    fs = FileLikeSocket(sock1)
    logger = FilteredLogger("Error", fs)
    logger.log("Warning: message number one")
    logger.log("Error: message number two")
    print("The socket received: %r" % sock2.recv(512))


"""
Python encourages duck typing, so an adapter's only responsibility
is to offer right methods.

Our adapters for ex. are exempt from the need to inherit from either
the classes they wrap or from the file type they are imitating.

Our adapters only need to impl the two file metds. that the Logger really uses.

"""

"""
SOLUTION 2:- BRIDGE PATTERN
The bridge pattern solves class explosion problem by switching
from inheritance to the object composition.

What this means is that you extract one of the dimensions into a
separate class hierarchy so that the original classes will reference
an object of the new hierarchy, instead of having all of its state
and behaviors within one class.

Read more at:- https://refactoring.guru/design-patterns/bridge
"""


# The “abstractions” that callers will see.
class Logger(object):
    def __init__(self, handler):
        self.handler = handler

    def log(self, message):
        self.handler.emit(message)


class FilteredLoggerBridge(Logger):
    def __init__(self, pattern, handler):
        self.pattern = pattern
        super().__init__(handler)

    def log(self, message):
        if self.pattern in message:
            super().log(message)


# The “implementations” hidden behind the scenes.


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


def filteredSocketLoggerUsingBridgePattern():
    handler = FileHandler(sys.stdout)

    logger = FilteredLoggerBridge("Error", handler)

    logger.log("Ignored: this will not be logged")
    logger.log("Error: this is important")


"""
SOLUTION 3:- DECORATOR PATTERN

What if we wanted to apply two different filters to the same log?

Neither of the above solutions supports multiple filters ---
say, one filtering by priority and the other matching a keyword.

But note the one place where the symmetry of this design breaks down:
- while filters can be stacked, output routines cannot be combined or stacked
- Log messages can still only be written to one output.
"""


class FileLoggerDecorator:
    def __init__(self, file):
        self.file = file

    def log(self, msg):
        self.file.write(msg + "\n")
        self.file.flush()


class SocketLoggerDecorator:
    def __init__(self, sock):
        self.sock = sock

    def log(self, message):
        self.sock.sendall((message + "\n").encode("ascii"))


class SyslogLoggerDecorator:
    def __init__(self, priority):
        self.priority = priority

    def log(self, message):
        syslog.syslog(self.priority, message)


# The filter calls the same method it offers.
class LogFilter:
    def __init__(self, pattern, logger):
        self.pattern = pattern
        self.logger = logger

    # Symmetric interface as of above loggers
    def log(self, message):
        if self.pattern in message:
            self.logger.log(message)


def FilteredLoggerDecorator():
    log1 = FileLoggerDecorator(sys.stdout)
    log2 = LogFilter("Error", log1)

    # Calling on main instance log method
    log1.log("Noisy: this logger always produces output")

    # calling log on filter class log method
    log2.log("Ignored: this will be filtered out")
    log2.log("Error: this is important and gets printed")

    # Stacking filter on top of each other
    log3 = LogFilter("severe", log2)

    log3.log("Error: this is bad, but not that bad")
    log3.log("Error: this is pretty severe")


if __name__ == "__main__":
    print("=========== CLASS EXPLOSION ===========")
    filteredLogger()
    print("======= AVOID CLASS EXPLOSION USING ADAPTER PATTERN =====")
    filteredSocketLoggerUsingAdapterPattern()
    print("======= AVOID CLASS EXPLOSION USING BRIDGE PATTERN =====")
    filteredSocketLoggerUsingBridgePattern()
    print("======= AVOID CLASS EXPLOSION USING DECORATOR PATTERN =====")
    FilteredLoggerDecorator()
