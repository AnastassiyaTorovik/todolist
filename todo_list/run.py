import logging

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column, String, Boolean, Date)
from flask_marshmallow import Marshmallow

# from todo_list.di import dependency_injection as di

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

    status = Column(
        'status', Boolean, nullable=False
    )

    deadline = Column(
        'deadline', Date, nullable=False
    )


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TaskModel


todo_schema = TaskSchema()
todos_schema = TaskSchema(many=True)


@app.route("/todos")
def todo_list():
    all_tasks = TaskModel.query.all()
    return jsonify(todos_schema.dump(all_tasks))


@app.route("/todo", methods=["POST"])
def add_task():
    new_task = TaskModel(task_id="Ukol1", text="some task", status=False, deadline='2022-11-30')
    db.session.add(new_task)
    db.session.commit()
    return jsonify("done"), 200


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8080)
