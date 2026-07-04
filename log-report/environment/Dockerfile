FROM python:3.11-slim-bookworm@sha256:c63fb9e02319f3900b991da7143e1177eb0c80b06b6b79753c13ff9543888365
WORKDIR /app
RUN pip install --no-cache-dir pytest pytest-json-ctrf
COPY environment/data/ /app/data/
COPY tests/ /app/tests/
