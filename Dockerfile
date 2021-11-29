FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy

COPY entrypoint.sh .
COPY . .

ENTRYPOINT ["bash", "/code/entrypoint.sh"]