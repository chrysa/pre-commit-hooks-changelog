FROM python:3.14-slim AS base
COPY . /src
WORKDIR /src
RUN pip install --quiet --upgrade pip

<<<<<<< HEAD
FROM base AS application
RUN pip install --quiet --editable .
=======
RUN set -x \
 && pip install -e .[pre_commit,push,tests]
>>>>>>> master

FROM application AS pytest
RUN pip install --quiet .[tests]

FROM application AS documentation
RUN pip install --quiet .[documentation]

FROM application AS quality
RUN pip install --quiet .[flake8,mypy,pylint]
