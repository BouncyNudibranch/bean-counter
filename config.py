import os
basedir = os.path.abspath(os.path.dirname(__file__))

ENV_DB = 'BEANCOUNTER_DATABASE_URI'
ENV_SKEY = 'BEANCOUNTER_SECRET_KEY'

try:
    SQLALCHEMY_DATABASE_URI = os.environ[ENV_DB]
except KeyError:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'bean_counter.db')

try:
    SECRET_KEY = os.environ[ENV_SKEY]
except KeyError:
    SECRET_KEY = 'qwertyuiop[]'

BEANS_PER_PAGE = 20
BREWS_PER_PAGE = 20
ROASTS_PER_PAGE = 20