FROM python:3.10

EXPOSE 7860/tcp

WORKDIR /app

RUN pip install pipenv

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv install

COPY main.py ./

CMD [ "pipenv", "run", "python", "./main.py" ]
