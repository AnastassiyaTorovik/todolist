import logging
from injector import Module, provider, singleton
from todo_list.configuration.postgresql_database import SessionLocal
from flask_injector import FlaskInjector

logger = logging.getLogger(__name__)


class ResourceModule(Module):
    @provider
    @singleton
    def get_db(self) -> SessionLocal:
        logger.info("Creating Postgresql session")
        return SessionLocal


def wire(flask_app):
    logger.info("Injecting dependencies to Flask application ...")
    return FlaskInjector(
        app=flask_app,
        modules=[ResourceModule])