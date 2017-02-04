#!/usr/bin/env python3

from paramecio.wsgiapp import app
from paramecio.index import run_app

application=app

if __name__ == "__main__":
    run_app(app)
