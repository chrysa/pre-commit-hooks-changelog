FROM python:3.14-slim AS base
COPY . /src
WORKDIR /src
RUN pip install --quiet --upgrade pip

FROM base AS application
# Editable install so coverage records repo-relative paths (pre_commit_hook/...)
# instead of site-packages paths, which SonarCloud cannot map to source files.
RUN pip install --quiet --editable .

FROM application AS pytest
RUN pip install --quiet -e ".[tests]"

FROM application AS documentation
RUN pip install --quiet .[documentation]

FROM application AS quality
RUN pip install --quiet .[flake8,mypy,pylint]
