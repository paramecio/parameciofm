#!/usr/bin/python3

from paramecio.index import create_app, run_app

app=create_app()

if __name__ == "__main__":
    run_app(app)