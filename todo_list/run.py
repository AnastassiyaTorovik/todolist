import logging

from flask import Flask

from todo_list.configuration.postgresql_database import engine
from todo_list.db_models.models import Base
from todo_list.di import dependency_injection as di

logger = logging.getLogger(__name__)
logging.captureWarnings(True)

Base.metadata.create_all(bind=engine)


app = Flask(__name__)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    # flask_injector = di.wire(app.app)