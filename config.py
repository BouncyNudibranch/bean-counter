"""
Bean Counter - Track Your Coffee!
Copyright (C) 2014  BonucyNudibranch (bouncynudibranch@gmail.com)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

ENV_DB = 'BEANCOUNTER_DATABASE_URI'
ENV_SKEY = 'BEANCOUNTER_SECRET_KEY'
ENV_BIND_IP = 'BEANCOUNTER_BIND_IP'
ENV_BIND_PORT = 'BEANCOUNTER_BIND_PORT'

try:
    SQLALCHEMY_DATABASE_URI = os.environ[ENV_DB]
except KeyError:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'bean_counter.db')

try:
    SECRET_KEY = os.environ[ENV_SKEY]
except KeyError:
    SECRET_KEY = 'qwertyuiop[]'

try:
    BIND_IP = os.environ[ENV_BIND_IP]
    BIND_PORT = int(os.environ[ENV_BIND_PORT])
except KeyError:
    BIND_IP = '127.0.0.1'
    BIND_PORT = 5000

BEANS_PER_PAGE = 20
BREWS_PER_PAGE = 20
ROASTS_PER_PAGE = 20