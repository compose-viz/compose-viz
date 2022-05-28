FROM python:alpine3.16 as builder

COPY ./ /compose-viz/

RUN \
    apk update && \
    pip install --upgrade pip

RUN \
    apk add binutils alpine-sdk libffi-dev

RUN \
    pip install poetry && \
    pip install pyinstaller

RUN \
    cd /compose-viz && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

RUN \
    cd /compose-viz && \
    pyinstaller --onefile --name cpv ./compose_viz/__main__.py

FROM alpine:3.16 as release

COPY --from=builder /compose-viz/dist/cpv /usr/local/bin/cpv

RUN \
    apk add --no-cache graphviz ttf-droid

VOLUME [ "/in" ]
WORKDIR "/in"

ENTRYPOINT [ "cpv" ]
