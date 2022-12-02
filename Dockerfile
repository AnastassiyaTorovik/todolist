FROM python:3.10-slim

WORKDIR /app

ENV POETRY_HOME="/opt/poetry"
# prepend poetry to path
ENV PATH="$POETRY_HOME/bin:$PATH"

COPY ./todo_list /app/todo_list
COPY ./poetry.lock /app/
COPY ./pyproject.toml /app/

RUN apt-get update \
    && apt-get -y install libpq-dev gcc netcat

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
RUN poetry build

EXPOSE 8080
# run entrypoint.sh
ENTRYPOINT ["/app/todo_list/entrypoint.sh"]
CMD ["python3", "todo_list/app"]