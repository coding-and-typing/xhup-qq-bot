FROM python:3.7-alpine

LABEL maintainer="ryan4yin <xiaoyin_c@qq.com>"

COPY . /xhup-club-api

WORKDIR /xhup-club-api

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk --no-cache add \
        build-base \
        libffi-dev \
        openssl-dev

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip install poetry hypercorn \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev \
    && pip uninstall poetry --yes \
    && rm -rf ~/.cache

ENTRYPOINT ["hypercorn", "run:bot.asgi"]

EXPOSE 8080