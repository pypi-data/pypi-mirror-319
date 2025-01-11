import enum
import functools
import pathlib

from descriptors import classonlymethod

import fate.conf


class ExitOnError:

    def __init__(self, parser):
        self.parser = parser

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, _traceback):
        if exc_type is None:
            return

        if issubclass(exc_type, fate.conf.MultiConfError):
            paths = ', '.join(exc_value.paths)
            self.parser.exit(64, f'{self.parser.prog}: error: multiple configuration file '
                                 f'formats at overlapping paths: {paths}\n')

        if issubclass(exc_type, fate.conf.ConfSyntaxError):
            self.parser.exit(65, f'{self.parser.prog}: error: could not decode '
                                 f'{exc_value.format.upper()}: {exc_value.decode_err}\n')

        if issubclass(exc_type, fate.conf.NoConfError):
            self.parser.exit(72, f'{self.parser.prog}: error: missing '
                                 f'configuration file (tried: {exc_value})\n')

        if issubclass(exc_type, (fate.conf.ConfTypeError, fate.conf.ConfValueError)):
            self.parser.exit(78, f'{self.parser.prog}: error: {exc_value}\n')


def exit_on_error(method):
    """Decorator to apply context manager `ExitOnError` to instance
    methods of classes of type `argcmdr.Command`.

    Note: The decorator wrapper depends upon instance attribute
    `parser`. As such, affected command classes must extend the default
    `__init__` (*i.e.* `super()`); or, decorated methods must be invoked
    *after* command initialization (*i.e.* not as part of its `__init__`).

    """
    @functools.wraps(method)
    def wrapped(self, *args, **kwargs):
        with ExitOnError(self.parser):
            return method(self, *args, **kwargs)

    return wrapped


class CommandInterface:

    class CommandStatus(enum.Enum):
        """Status categories of task command return codes."""

        # typical exit codes
        Retry = 42  # framework-specific
        OK = 0

        # termination by signal
        Killed = -9
        Terminated = -15

        # meta-statuses for erroneous exits
        Unrecognized = -997
        Timeout = -998
        Error = -999

        @classonlymethod
        def select(cls, code):
            """Retrieve appropriate status for given return code."""
            value = int(code)

            try:
                return cls(value)
            except ValueError:
                return cls.Error if value > 0 else cls.Unrecognized

        @classonlymethod
        def assign(cls, code, stopped=False):
            """Retrieve appropriate status given return code and whether
            a Timeout stop was issued.

            """
            status = cls.select(code)
            return cls.Timeout if stopped and status.stoppage else status

        @property
        def erroneous(self) -> bool:
            return self.value < 0

        @property
        def stoppage(self) -> bool:
            return -100 < self.value < 0

        def __str__(self):
            return self.name

    @property
    def conf(self):
        if (root := self.root) is None:
            # this is the root command
            # retrieve and store conf here
            try:
                conf = self.__dict__['conf']
            except KeyError:
                conf = self.__dict__['conf'] = self.args.__conf__ or fate.conf.get()

            return conf

        # defer to root
        return root.conf

    @property
    def exit_on_error(self):
        return ExitOnError(self.parser)

    @staticmethod
    def write_result(path: pathlib.Path, contents: bytes):
        if path.exists():
            raise FileExistsError(path)

        if not path.parent.exists():
            try:
                path.parent.mkdir(parents=True)
            except NotADirectoryError:
                pass

        if not path.parent.is_dir():
            raise NotADirectoryError(20, 'Not a directory', path.parent)

        path.write_bytes(contents)
