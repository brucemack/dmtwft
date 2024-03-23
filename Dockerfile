FROM python:3.11.2-slim-bullseye

# Setup virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Install dependencies:
COPY requirements.txt .
# The pip command is controlled by PATH (so uses venv)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY main.py .
COPY __init__.py .

RUN mkdir -p utils
COPY utils/__init__.py utils
COPY utils/convert.py utils
COPY utils/DTMF.py utils
COPY utils/parse.py utils
COPY utils/Token.py utils

RUN mkdir -p www

RUN mkdir -p www/assets
COPY www/assets/index.css www/assets
COPY www/assets/index.js www/assets
COPY www/assets/logo.png www/assets

RUN mkdir -p www/templates
COPY www/templates/index.html www/templates

# The uvicorn command is controller by PATH (so uses venv)
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080" ]
