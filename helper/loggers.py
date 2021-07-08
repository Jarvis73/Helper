import logging
from pathlib import Path
from time import time, strftime, localtime

levels = [logging.NOTSET,
          logging.DEBUG,
          logging.INFO,
          logging.WARNING,
          logging.ERROR,
          logging.CRITICAL]


class Logger(object):
    _log = logging.getLogger()
    default = True

    def debug(self, *args, **kwargs):
        self._log.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self._log.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self._log.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self._log.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self._log.critical(*args, **kwargs)


# We create a global logger. This statement is only executed once.
logger = Logger()


def create_logger(file_=False, console=True,
                  with_time=False, file_level=1, console_level=2,
                  propagate=False, clear_exist_handlers=False, name=None):
    """ Create a logger to write info to console and file.

    Parameters
    ----------
    file_: bool or str
        write message to a file or not. If True, filename will be a timestamp;
        If a string, it will be the exact filename.
    console: bool
        write info to console or not
    with_time: bool
        if set, a timestamp will be added as a prefix of log_file when `file_`
        is a string.
    file_level: int
        log level to the file
    console_level: int
        log level to the console
    propagate: bool
        if set, then message will be propagate to root logger
    clear_exist_handlers: bool
        clear exist handlers
    name: str
        logger name, if None, then root logger will be used

    Note
    ----
    * Do not set propagate flag and give a name to the logger is the way
    to avoid logging dublication.
    * use code snippet below to change the end mark "\n"
    ```
    for hdr in logger.handlers:
        hdr.terminator = ""
    ```

    Returns
    -------
    A logger object of class getLogger()
    """
    if file_level < 0 or file_level > 5:
        raise ValueError(f"`file_level` must be an integer range from 0 to 5,"
                         f" got {file_level}")
    if console_level < 0 or console_level > 5:
        raise ValueError(f"`console_level` must be an integer range from 0 to"
                         f" 5, got {file_level}")

    if file_:
        prefix = strftime('%Y%m%d_%H%M%S', localtime(time()))
        if file_ is True:
            log_file = Path(__file__).parent / f"{prefix}.log"
        elif isinstance(file_, str):
            log_file = Path(file_)
            if with_time:
                log_file = log_file.with_name(f"{prefix}_{log_file.name}")
        else:
            raise TypeError("`file_` must be a bool flag or a string of the"
                            " log file name.")
        if not log_file.parent.exists():
            log_file.parent.mkdir(parents=True, exist_ok=True)

    logger_ = logging.getLogger(name)

    if clear_exist_handlers:
        logger_.handlers.clear()

    logger_.setLevel(levels[1])
    logger_.propagate = propagate

    formatter = MyFormatter("%(asctime)s %(levelname).1s %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")

    if file_:
        # Create file handler
        file_handler = logging.FileHandler(str(log_file))
        file_handler.setLevel(levels[file_level])
        file_handler.setFormatter(formatter)
        # Register handler
        logger_.addHandler(file_handler)

    if console:
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(levels[console_level])
        console_handler.setFormatter(formatter)
        logger_.addHandler(console_handler)

    return logger_


def get_global_logger(name="default", **kwargs):
    global logger
    if logger.default:
        logger._log = create_logger(name=name, **kwargs)
        logger.default = False
    return logger


class C(object):
    """
    Colored command line output formatting
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def c(string, color):
        """ Change color of string """
        return color + string + C.ENDC


def test_Color():
    print(C.c("Header", C.HEADER))
    print("Processing ...", C.c("OK", C.OKBLUE))
    print("Processing ...", C.c("OK", C.OKGREEN))
    print(C.c("Warning", C.WARNING))
    print(C.c("Failed", C.FAIL))
    print(C.c("Bold", C.BOLD))
    print(C.c("Underline", C.UNDERLINE))
