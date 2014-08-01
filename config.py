import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'bean_counter.db')
SECRET_KEY = 'qwertyuiop[]'

BEANS_PER_PAGE = 20
BREWS_PER_PAGE = 20
ROASTS_PER_PAGE = 20