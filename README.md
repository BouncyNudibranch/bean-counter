# Bean Counter - Track Your Coffee!

## Overview
This web application is designed to be used by coffee enthusiasts who want a simple interface to store and track
information about their bean purchases, roasting techniques, and brewing methods.

## Installation
This application is designed to work with Python 2.7.

1. Clone the repository `git clone https://github.com/BouncyNudibranch/bean-counter.git`
2. Install required libraries `pip install -r requirements.txt`
3. Create a new database `python create_db.py`
4. Run the application `python run.py`

## Configuration
Please have a look at `config.py` for most of the configurable aspects of the application. There are a few environment
variables you can set:

* `BEANCOUNTER_DATABASE_URI` should contain the path to the sqlite database file. Defaults to app root.
* `BEANCOUNTER_SECRET_KEY` is used by Flask to create cookies. Defaults to `qwertyuiop[]`.
* `BEANCOUNTER_BIND_IP` is the IP address to which Flask will bind. Defaults to `127.0.0.1`.
* `BEANCOUNTER_BIND_PORT` is the port to which Flask will bind. Defaults to `5000`.