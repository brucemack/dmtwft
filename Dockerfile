FROM python:3.12

# Setup virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# The pip command is controlled by PATH (so uses venv)
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
# Install dependencies:
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# ----- Application Build ----------------------------------------------------
COPY main.py .
COPY log_conf.yaml .

RUN mkdir -p utils
COPY utils/*.py utils

RUN mkdir -p www

RUN mkdir -p www/assets
COPY www/assets/index.css www/assets
COPY www/assets/index.js www/assets
COPY www/assets/logo.png www/assets

RUN mkdir -p www/templates
COPY www/templates/index.html www/templates

# ----- Application Run ------------------------------------------------------
# The uvicorn command is controller by PATH (so uses venv)
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--log-config=log_conf.yaml" ]
