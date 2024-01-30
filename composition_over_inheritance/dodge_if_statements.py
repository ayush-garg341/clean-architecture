"""
When a new design requirement appears,
does the typical Python programmer really go write a new class?
- NO

Simple is better than complex.
Why add a class, when an if statement will work instead.

A single logger class can gradually accrete conditionals until
it handles all the same cases as our previous examples:
"""
import sys
import syslog


# Each new feature as an “if” statement.
class Logger:
    def __init__(self, pattern=None, file=None, sock=None, priority=None):
        self.pattern = pattern
        self.file = file
        self.sock = sock
        self.priority = priority

    def log(self, message):
        if self.pattern is not None:
            if self.pattern not in message:
                return
        if self.file is not None:
            self.file.write(message + "\n")
            self.file.flush()
        if self.sock is not None:
            self.sock.sendall((message + "\n").encode("ascii"))
        if self.priority is not None:
            syslog.syslog(self.priority, message)


# Works just fine.

logger = Logger(pattern="Error", file=sys.stdout)

logger.log("Warning: not that important")
logger.log("Error: this is important")


"""
We may recognize this example as more typical of the Python
design practices we’ve encountered in real applications.

but this approach is not without benefits, this class’s whole range of possible
behaviors can be grasped in a single reading of the code from top to bottom.
"""
