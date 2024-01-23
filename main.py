import time
import logging


def retry_on_exception(exceptions, max_attempts):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    return result
                except exceptions as e:
                    if attempt < max_attempts:
                        logging.warning(f"Attempt {attempt} failed. Retrying in 1 second...")
                        time.sleep(1)
                    else:
                        logging.error(f"All attempts failed. Logging the exception and re-raising.")
                        logging.exception(e)
                        raise
        return wrapper
    return decorator


@retry_on_exception((ZeroDivisionError, KeyError), max_attempts=3)
def risky_operation(x, y):
    return x / y


result = risky_operation(10, 0)

