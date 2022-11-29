import logging

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger(__name__)
logging.captureWarnings(True)

app = Flask(__name__)
app.config.from_object("todo_list.configuration.postgresql_database.Config")
db = SQLAlchemy(app)


class Tasks(db.Model):
    __tablename__ = 'TASKS'

    __table_args__ = ()

    task_id = db.Column(
        'task_id', db.String(36), primary_key=True, unique=True, nullable=False
    )

    text = db.Column(
        'text', db.String(255), nullable=False
    )

    status = db.Column(
        'status', db.Boolean, nullable=False
    )

    deadline = db.Column(
        'deadline', db.Date, nullable=False
    )


@app.route("/add_task", methods=["POST"])
def add_task():
    new_task = Tasks(task_id="Ukol1", text="some task", status=False, deadline='2022-11-30')
    db.session.add(new_task)
    db.session.commit()
    return jsonify("done"), 200


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8080)