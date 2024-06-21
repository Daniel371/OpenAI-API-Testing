FROM python:3.11-bullseye

WORKDIR /workspace

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  gcc \
  freetds-dev \
  unixodbc-dev \
  curl \
  gnupg \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get update

  RUN pip install --upgrade pip && pip install pipenv

  COPY Pipfile* ./
  
  # Install dependencies
  RUN  pip install pipenv && \
    pipenv lock && pipenv requirements > requirements.txt && \
    pip install -r requirements.txt
    
  RUN pip install fastapi[all] fastapi-cli
# Just keep container running
CMD ["tail", "-f", "/dev/null"]
