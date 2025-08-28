#!/bin/bash

set -e 

if [ -f "app.py" ]; then

    # runserver
    flask run

else
    echo "Flask project not installed or incomplete — app.py file missing"
    echo "Please create the project"
    exec tail -f /dev/null
fi

exec "$@"
