FROM python:3.10

# Python runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV FLASK_DEBUG=0
ENV FLASK_APP=app:app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# requirements
COPY requirements/base.txt /tmp/requirements/base.txt
COPY requirements/prod.txt /tmp/requirements/prod.txt
RUN pip install -r /tmp/requirements/prod.txt
RUN rm -rf /tmp/requirements

# entrypoint
COPY entrypoints/prod/flask-entrypoint.sh /usr/local/bin/entrypoints/flask-entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoints/flask-entrypoint.sh

# env
COPY env/prod/flask-env.sh /etc/flask/flask-env.sh
RUN chmod +x /etc/flask/flask-env.sh

# project workdir
WORKDIR /app
COPY ./app /app

# user
ARG USERNAME=flask
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
USER $USERNAME

ENTRYPOINT ["/usr/local/bin/entrypoints/flask-entrypoint.sh"]

EXPOSE 8080
