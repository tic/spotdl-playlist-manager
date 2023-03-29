import builtins as __builtin__
from datetime import datetime

time = lambda : datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
default_print = print
__builtin__.print = lambda *args, **kwargs : default_print(f'[{time()}]', *args, **kwargs)
