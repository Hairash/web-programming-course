FROM python:3.13.2 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

COPY 9_websocket/requirements.txt ./
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

FROM python:3.13.2-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY 9_websocket .

CMD ["python", "9_websocket/server.py"]
