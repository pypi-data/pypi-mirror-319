from rich import print

PREFIX = {key: "[#666666]\\[[/]" + value + "[#666666]]:[/]" for key, value in {
        "exception": "[bold red]E[/]",
        "critical": "[bold red]C[/]",
        "error": "[bold red]![/]",
        "success": "[bold green]+[/]",
        "warning": "[bold yellow]⚠[/]",
        "info": "[bold blue]i[/]",
        "verbose": "[bold pink]v[/]",
        "debug": "[bold #666666]d[/]",
        }.items()}

LOG_LEVELS = {
        "exception": -1,
        "critical": -1,
        "error": 0,
        "success": 1,
        "warning": 2,
        "info": 3,
        "verbose": 4,
        "debug": 5,
        }

LOGLEVEL = 3

def _render(level, message, prefix='', suffix=''):
    return f"{PREFIX[level]}{prefix} {message}{suffix}"

def _log(message, level="info", force=False, prefix='', suffix='', _func=print, **kwargs):
    if LOG_LEVELS[level] <= LOGLEVEL or force:
        _func(_render(level, message, prefix=prefix, suffix=suffix), **kwargs)

def exception(message, **kwargs):
    _log(message, "exception", **kwargs)

def critical(message, **kwargs):
    _log(message, "critical", **kwargs)

def error(message, **kwargs):
    _log(message, "error", **kwargs)

def success(message, **kwargs):
    _log(message, "success", **kwargs)

def warning(message, **kwargs):
    _log(message, "warning", **kwargs)

def info(message, **kwargs):
    _log(message, "info", **kwargs)

def verbose(message, **kwargs):
    _log(message, "verbose", **kwargs)

def debug(message, **kwargs):
    _log(message, "debug", **kwargs)

def set_loglevel(level):
    global LOGLEVEL
    LOGLEVEL = level
    
