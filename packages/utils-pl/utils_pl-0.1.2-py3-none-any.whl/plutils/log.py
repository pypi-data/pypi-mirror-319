import logging
from rich.logging import RichHandler

_LOG_LEVEL = logging.NOTSET
_LOGGERS = set()

def set_loglevel(level):
    global _LOG_LEVEL
    _LOG_LEVEL = level
    for logger in _LOGGERS:
        logger.setLevel(_LOG_LEVEL)

console_format = '%(message)s'
logging.basicConfig(
    level="NOTSET",
    format=console_format,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False, show_path=False, show_level=False)],
)
rich_log = logging.getLogger("rich")

_PREFIX = {
    key: f"[#666666]\\[[/]{value}[#666666]]:[/]" for key, value in {
        "exception": "[bold red]E[/]",
        "critical": "[bold red]C[/]",
        "error": "[bold red]![/]",
        "success": "[bold green]+[/]",
        "warning": "[bold yellow]⚠[/]",
        "info": "[bold blue]i[/]",
        "verbose": "[bold pink]v[/]",
        "debug": "[bold #666666]#[/]",
    }.items()
}

class Logger(logging.Logger):
    def __init__(self, name, color: str | None = None, level = None):
        level = level or _LOG_LEVEL
        super().__init__(name, level)
        self.color = color or "#666666"
        self.name_append = f"[{color}]{self.name}[/]"

        self.handler = RichHandler(rich_tracebacks=True, show_time=False, show_path=False, show_level=False)
        self.addHandler(self.handler)

        _LOGGERS.add(self)

    @staticmethod
    def __render(prefix):
        """
        Decorator that renders the message with the given prefix
        """
        if prefix not in _PREFIX:
            raise ValueError(f"Invalid prefix: must be of {_PREFIX.keys()} but got {prefix}")
        def wrapper(func):
            def inner(self, msg, *args, **kwargs):
                rendered = f"{self.name_append} {_PREFIX[prefix]} {msg}"
                return func(self, rendered, *args, **kwargs)
            return inner
        return wrapper

    @__render("info")
    def info(self, msg, *args, **kwargs):
        rich_log.info(msg, *args, **kwargs, extra={"markup": True, "highlighter": None})

    @__render("error")
    def error(self, msg, *args, **kwargs):
        rich_log.error(msg, *args, **kwargs, extra={"markup": True, "highlighter": None})

    @__render("success")
    def success(self, msg, *args, **kwargs):
        rich_log.info(msg, *args, **kwargs, extra={"markup": True, "highlighter": None})

    @__render("warning")
    def warning(self, msg, *args, **kwargs):
        rich_log.warning(msg, *args, **kwargs, extra={"markup": True, "highlighter": None})

    @__render("exception")
    def exception(self, msg, *args, **kwargs):
        rich_log.exception(msg, *args, **kwargs, extra={"markup": True, "highlighter": None})

    @__render("critical")
    def critical(self, msg, *args, **kwargs):
        rich_log.critical(msg, *args, **kwargs, extra={"markup": True, "highlighter": None})

    @__render("verbose")
    def verbose(self, msg, *args, **kwargs):
        raise NotImplementedError("Verbose logging is not implemented yet")

    @__render("debug")
    def debug(self, msg, *args, **kwargs):
        rich_log.debug(msg, *args, **kwargs, extra={"markup": True, "highlighter": None})

    def print(self, msg, *args, level = logging.INFO, **kwargs):
        self._log(level, msg, args, **kwargs)

    def _log(self, level, msg, *args, **kwargs):
        rich_log.log(level, msg, *args, **kwargs, extra={"markup": True, "highlighter": None})
