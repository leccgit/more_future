#!/bin/sh
exec gunicorn -b 0.0.0.0:5050 --access-logfile - --error-logfile - marketplace:app

