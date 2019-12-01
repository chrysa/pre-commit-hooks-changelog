FROM python:3.7

COPY . /src

WORKDIR /src

RUN set -x \
 && pip install -q -r requirements-dev.txt \
 && pip install -e .

VOLUME ["/src"]
