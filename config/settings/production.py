from .base import *
import environ

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = False
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = ['.pythonanywhere.com']