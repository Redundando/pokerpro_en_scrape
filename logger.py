import time


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @staticmethod
    def bold(text):
        return Color.BOLD + text + Color.END


def log(fn):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        to_execute = fn(*args, **kwargs)
        args_string = str(args)
        if len(args_string) > 100:
            args_string = args_string[0:100] + "..."
        kwargs_string = str(kwargs)
        if len(kwargs_string) > 100:
            kwargs_string = kwargs_string[0:100] + "..."

        end = time.perf_counter()
        print(
            f'{Color.bold(fn.__name__)} ({args_string} {kwargs_string})\nTime: {round(end - start, 5)}s\n==========')
        return to_execute

    return inner
