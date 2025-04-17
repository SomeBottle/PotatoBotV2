FROM bitnami/python:3.10.16

LABEL maintainer="Somebottle"

ENV PIP_INSTALL_BIN_DIR="/home/somebottle/.local/bin" \
    BITNAMI_PYTHON_BIN_DIR="/opt/bitnami/python/bin"

USER root

WORKDIR /app

RUN useradd -m -s /bin/bash somebottle && \
    echo 'export PATH=$PATH:'$PIP_INSTALL_BIN_DIR >/etc/profile.d/python.sh && \
    echo 'export PATH=$PATH:'$BITNAMI_PYTHON_BIN_DIR >>/etc/profile.d/bitnami.sh && \
    chown -R somebottle:somebottle /app

USER somebottle

COPY . /app

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python","/app/main.py"]
