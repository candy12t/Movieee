from .settings_common import *


DEBUG = True

ALLOWED_HOSTS = []

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # ログフォーマット
    'formatters': {
        # 開発用
        'develop': {
            'format': '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d'
                      '%(message)s'
        },
    },

    # ハンドラ
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'develop',
        },
    },

    # ロガー
    'loggers': {
        # movieeeアプリケーションのロガー
        'movieee': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },

        # Django本体のロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}