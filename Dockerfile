FROM python:3.13.3-slim

# Install PostgreSQL development dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man

WORKDIR /app
COPY . /app

RUN pip install .

EXPOSE 8000
