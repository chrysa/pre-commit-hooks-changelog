FROM  python:3.8-slim as base
COPY . /src
WORKDIR /src

FROM scratch as application
COPY --from=base / /
WORKDIR /src
RUN pip install --quiet --editable .

FROM scratch as pytest
COPY --from=application / /
WORKDIR /src
RUN pip install --quiet .[tests]

FROM scratch as documentation
COPY --from=application / /
WORKDIR /src
RUN set -x \
  && pip install --quiet .[documentation]

FROM scratch as quality
COPY --from=application / /
WORKDIR /src
RUN set -x \
  && pip install --quiet .[flake8,mypy,pylint]
