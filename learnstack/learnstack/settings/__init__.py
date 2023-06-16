from .base import *
from decouple import config
import os

APP_ENV= config('APP_ENV')

if config('APP_ENV') == 'prod':
    from .prod import *
else:
    from .dev import *