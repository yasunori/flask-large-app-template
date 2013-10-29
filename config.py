# vim:fileencoding=utf8
import logging
from os import path

CONFIG = {}
MODE = 'DEVELOPMENT'


def set_mode(mode):
    global MODE
    MODE = mode


def get_app_conf(mode):
    global CONFIG
    if CONFIG:
        return CONFIG

    my_path = path.dirname(path.abspath(__file__))
    CONFIG = {
        'DEBUG': False,
        'TESTING': False,
        'WTF_CSRF_ENABLED': False,
        'SESSION_OPTIONS': {
            'session.type': 'file',
            'session.data_dir': my_path + '/webapp/tmp',
            'session.cookie_expires': 86400,
            'session.auto': True
        },
        'DB': {
            'DSN': 'postgresql://developer:@localhost:5432/testpy',
            'AUTO_COMMIT': False,
            'AUTO_FLUSH': True
        },
    }

    if(mode == 'PRODUCTION'):
        pass

    if(mode == 'DEVELOPMENT'):
        CONFIG['DEBUG'] = True
        CONFIG['DB']['DSN'] = 'postgresql://developer:@localhost:5432/testpy'

    if(mode == 'TESTING'):
        CONFIG['TESTING'] = True
        CONFIG['DB']['DSN'] = 'postgresql://developer:@localhost:5432/testpy_test'

    return CONFIG


def set_log_conf(mode):
    LOGGING_STERAM_FLG = False
    LOGGING_STERAM_LEVEL = logging.CRITICAL
    LOGGING_FILE_FLG = True
    LOGGING_FILE_LEVEL = logging.WARNING

    if(mode == 'PRODUCTION'):
        pass

    if(mode == 'DEVELOPMENT'):
        LOGGING_STERAM_FLG = True
        LOGGING_STERAM_LEVEL = logging.CRITICAL
        LOGGING_FILE_FLG = True
        LOGGING_FILE_LEVEL = logging.DEBUG

    if(mode == 'TESTING'):
        LOGGING_STERAM_FLG = False
        LOGGING_STERAM_LEVEL = logging.CRITICAL
        LOGGING_FILE_FLG = True
        LOGGING_FILE_LEVEL = logging.DEBUG

    '''
    ログの設定
    app.logging は使わない方針。appコンテキスト外でもログ出すので
    '''
    LOGGING_FILE_NAME = path.dirname(path.abspath(__file__)) + '/webapp/log/app.log'

    if LOGGING_STERAM_FLG:
        stream_log = logging.StreamHandler()
        stream_log.setLevel(LOGGING_STERAM_LEVEL)
        stream_log.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(process)d %(pathname)s %(lineno)d %(message)s'))
        logging.getLogger().addHandler(stream_log)

    if LOGGING_FILE_FLG:
        file_log = logging.FileHandler(filename=LOGGING_FILE_NAME)
        file_log.setLevel(LOGGING_FILE_LEVEL)
        file_log.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(process)d %(pathname)s %(lineno)d %(message)s'))
        logging.getLogger().addHandler(file_log)

    #rootロガーのログレベル（最低にしておく)
    logging.getLogger().setLevel(logging.DEBUG)
