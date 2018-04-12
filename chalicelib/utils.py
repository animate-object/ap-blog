from functools import wraps
from traceback import print_exc

def handle_errors(f):
    @wraps(f)
    def handle_errors_wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            print_exc()
            raise
    return handle_errors_wrapper
