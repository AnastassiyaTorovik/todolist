import logging
from pydantic import ValidationError

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column, String, Boolean, Date)
from sqlalchemy.exc import IntegrityError
from flask_marshmallow import Marshmallow

from todo_list.validators.input_validators import TaskValidator
from todo_list.helpers.exceptions import get400, get404


logger = logging.getLogger(__name__)
logging.captureWarnings(True)

app = Flask(__name__)

app.config.from_object("todo_list.configuration.postgresql_database.Config")
db = SQLAlchemy(app)
ma = Marshmallow(app)


class TaskModel(db.Model):
    __tablename__ = 'TASKS'

    __table_args__ = ()

    task_id = Column(
        'task_id', String(36), primary_key=True, unique=True, nullable=False
    )

    text = Column(
        'text', String(255), nullable=False
    )

    is_done = Column(
        'status', Boolean, nullable=False
    )

    deadline = Column(
        'deadline', Date, nullable=False
    )


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TaskModel


# needed for objects serialization
todo_schema = TaskSchema()
todos_schema = TaskSchema(many=True)


@app.route("/todos")
def get_todo_list():
    all_tasks = TaskModel.query.all()
    return jsonify(todos_schema.dump(all_tasks))


@app.route("/todo", methods=["POST"])
def post_task():
    task_body = request.json
    try:
        task_body = TaskValidator(**task_body).dict()
    except (ValidationError, ValueError) as e:
        return get400(f'{e}').message
    new_task = TaskModel(**task_body)
    db.session.add(new_task)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return get400(f'Unique constraint violation. Todo with the same id "{new_task.task_id}" already exists').message
    return jsonify("Todo has been added"), 201


@app.route("/<task_id>/set-done", methods=["PUT"])
def put_status_done(task_id):
    task = TaskModel.query.filter_by(task_id=task_id).first()
    if not task:
        return get404('Task not found').message
    task.is_done = True
    db.session.commit()
    return jsonify(f"{task_id} is set to done"), 200


@app.route("/<task_id>/set-not-done", methods=["PUT"])
def put_status_not_done(task_id):
    task = TaskModel.query.filter_by(task_id=task_id).first()
    if not task:
        return get404('Task not found').message
    task.is_done = False
    db.session.commit()
    return jsonify(f"{task_id} is set to not done"), 200


@app.route("/todo/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = TaskModel.query.filter_by(task_id=task_id).first()
    if not task:
        return get404('Task not found').message
    db.session.delete(task)
    db.session.commit()
    return jsonify(), 204


if __name__ == "__main__":
    logger.info('Starting application')
    app.run(host="0.0.0.0", port=8080)

