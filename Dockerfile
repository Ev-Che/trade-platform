FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .

RUN pip install --upgrade pip
RUN pip install pipenv

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy

ENTRYPOINT ["bash", "entrypoint.sh"]