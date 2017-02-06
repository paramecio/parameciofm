#!/bin/sh

gunicorn -w1 --reload --bind localhost:8080 index:app

