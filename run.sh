#!/usr/bin/env bash
#Starts the app in debug mode - automatically updates when code changes
export FLASK_APP=music_logger.py
export FLASK_DEBUG=1
flask run
