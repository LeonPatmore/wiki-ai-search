FROM python:3.10

EXPOSE 8080/tcp
EXPOSE 8082/tcp
EXPOSE 8084/tcp

WORKDIR /app

RUN pip install pipenv

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv install

COPY main.py ./
COPY ai_search.py ./
COPY rest_api.py ./
COPY search.py ./
COPY slack_event_listener.py ./
COPY web_interface.py ./
COPY web_server.py ./

CMD [ "pipenv", "run", "python", "./main.py" ]
