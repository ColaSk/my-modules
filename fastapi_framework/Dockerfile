FROM python:3.8-slim-buster

ENV TZ=Asia/Shanghai LANG=C.UTF-8

VOLUME ["/home/project", "/home/logs"]

WORKDIR /home/project

COPY ./mirrors /mirrors

RUN cp /mirrors/sources.list /etc/apt/sources.list && \
    apt update && apt upgrade -y && \
    apt autoclean -y && apt autoremove -y && \
    apt install gcc -y && \
    python -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/ && \
    pip3 install -r /mirrors/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir