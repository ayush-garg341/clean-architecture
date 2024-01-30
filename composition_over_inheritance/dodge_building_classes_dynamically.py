"""
Python offers a workaround to avoid a proliferation of classes.

Imagine that our application reads a configuration file to learn
the log filter and log destination it should use, a file whose contents
aren’t known until runtime.

Instead of building all m×n possible classes ahead of time and then selecting
the right one, we can wait and take advantage of the fact that Python not only
supports the class statement but a builtin type() function that creates new
classes dynamically at runtime:
"""


class FileLogger:
    def __init__(self, file):
        self.file = file

    def log(self, msg):
        self.file.write(msg + "\n")
        self.file.flush()


class SocketLogger:
    def __init__(self, sock):
        self.sock = sock

    def log(self, message):
        self.sock.sendall((message + "\n").encode("ascii"))


# The filter calls the same method it offers.
class LogFilter:
    def __init__(self, pattern, logger):
        self.pattern = pattern
        self.logger = logger

    # Symmetric interface as of above loggers
    def log(self, message):
        if self.pattern in message:
            self.logger.log(message)


filters = {
    "pattern": LogFilter,
}
outputs = {
    "file": FileLogger,
    "socket": SocketLogger,
}

# Select the two classes we want to combine.

with open("config") as f:
    filter_name, output_name = f.read().split()

filter_cls = filters[filter_name]
output_cls = outputs[output_name]

# Build a new derived class (!)

name = filter_name.title() + output_name.title() + "Log"
cls = type(name, (filter_cls, output_cls), {})

# Call it as usual to produce an instance.

logger = cls(...)

"""
The tuple of classes passed to type() has the same meaning as series of base
classes in a class statement. The type() call above creates a new class
through multiple inheritance from both a filtered logger and an output logger.
"""
