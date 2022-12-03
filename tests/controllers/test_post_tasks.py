import json
from datetime import datetime

from tests.sqlite_config import SQLiteConfig
from todo_list.app import TaskModel


class TestPostTask(SQLiteConfig):
    def test_post_task(self):
        request_data = {"task_id": "test_1", "deadline": "2022-12-31", "text": "to pass test"}
        # put data into memory
        response = self.client.post('/todo', data=json.dumps(request_data), content_type='application/json')
        self.assertStatus(response, 201)

        # check database
        self.assertEqual(1, TaskModel.query.count())
        new_task = TaskModel.query.filter_by(task_id=request_data.get('task_id')).first()
        self.assertIsNotNone(new_task)
        self.assertEqual(datetime.strptime(request_data.get('deadline'), '%Y-%m-%d').date(), new_task.deadline)
        self.assertEqual(request_data.get('task_id'), new_task.task_id)
        self.assertEqual(request_data.get('text'), new_task.text)
        self.assertEqual(False, new_task.is_done)

    def test_duplicate_insert(self):
        request_data = {"task_id": "test_1", "deadline": "2022-12-15", "text": "to do something"}
        for _ in range(2):
            response = self.client.post('/todo', data=json.dumps(request_data), content_type='application/json')

        # the last response is tested
        self.assertStatus(response, 400)
        self.assertEqual(response.json['title'], 'Bad Request')
        self.assertIn('unique constraint violation', response.json['detail'].lower())
        self.assertEqual(1, TaskModel.query.count())

    def test_incorrect_task_id(self):
        request_data = {"task_id": "něco_2*", "deadline": "2022-12-15", "text": "to do something"}
        response = self.client.post('/todo', data=json.dumps(request_data), content_type='application/json')
        self.assertStatus(response, 400)
        self.assertIn('can only contain characters [a-zA-Z0-9_]', response.json['detail'])
        self.assertEqual(0, TaskModel.query.count())

    def test_wrong_date_format(self):
        request_data = {"task_id": "test_1", "deadline": "15.12.2022", "text": "to do something"}
        response = self.client.post('/todo', data=json.dumps(request_data), content_type='application/json')
        self.assertStatus(response, 400)
        self.assertIn('%Y-%m-%d', response.json['detail'])

    def test_too_long_text(self):
        request_data = {"task_id": "test_1", "deadline": "2022-12-31", "text": f"{'to_do'*400}"}
        response = self.client.post('/todo', data=json.dumps(request_data), content_type='application/json')
        self.assertStatus(response, 400)
        self.assertIn('255 characters', response.json['detail'])

    def test_missing_required_field(self):
        request_data = {"task_id": "test_1", "text": "todo", "is_done": True}
        response = self.client.post('/todo', data=json.dumps(request_data), content_type='application/json')
        self.assertStatus(response, 400)
        self.assertIn('deadline', response.json['detail'])



