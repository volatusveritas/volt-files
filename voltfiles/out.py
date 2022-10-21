from voltfiles import colors


MESSAGE_PADDING_SIZE: int = 4


def out(message: str) -> None:
    print(" " * MESSAGE_PADDING_SIZE + message)


def info(message: str) -> None:
    out(colors.INFO + message)


def warning(message: str) -> None:
    out(colors.WARNING + message)


def error(message: str) -> None:
    out(colors.ERROR + message)
