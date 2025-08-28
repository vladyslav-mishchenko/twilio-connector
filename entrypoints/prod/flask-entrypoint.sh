#!/bin/bash

set -e 

if [ -f "app.py" ]; then

    # env
    source /etc/flask/flask-env.sh

    # runserver
    gunicorn "$FLASK_APP" \
    --bind "$FLASK_RUN_HOST:$FLASK_RUN_PORT" \
    --workers 4 \
    --timeout 30 \
    --log-level info

else
    echo "Flask project not installed or incomplete — app.py file missing"
    echo "Please create the project"
    exec tail -f /dev/null
fi

exec "$@"
