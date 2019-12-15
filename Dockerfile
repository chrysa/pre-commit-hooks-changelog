FROM python:3.7

COPY . /src

WORKDIR /src

RUN set -x \
 && pip install -e .[pre_commit,push,tests]

VOLUME ["/src"]
