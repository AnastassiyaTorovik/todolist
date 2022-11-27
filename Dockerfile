FROM python:3.10-slim

WORKDIR /app

COPY ./todo_list /app/todo_list
COPY ./poetry.lock /app/
COPY ./pyproject.toml /app/

ENV POETRY_HOME="/opt/poetry"
#ENV PATH="${PATH}:/root/.poetry/bin"
# prepend poetry to path
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
RUN poetry build

EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/python3.10"]
CMD ["todo_list/run.py"]