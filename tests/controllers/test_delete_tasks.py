import json

from tests.sqlite_config import SQLiteConfig

from todo_list.app import TaskModel


class TestGetTask(SQLiteConfig):
    def popupate_database(self):
        request_data = [
            {
                "task_id": "test_1", "deadline": "2022-11-29", "text": "smth important 1"
            }
        ]
        for todo in request_data:
            response = self.client.post('/todo', data=json.dumps(todo), content_type='application/json')
            self.assertStatus(response, 201)

        # check if all records have been populated
        self.assertEqual(1, TaskModel.query.count())

    def test_delete_task(self):
        self.popupate_database()
        response = self.client.delete('/todo/test_1', content_type='application/json')
        self.assertStatus(response, 204)

        # check if task deleted
        response = self.client.get('todos', content_type='application/json')
        self.assert200(response)
        self.assertEqual(0, len(response.json))

    def test_delete_task_not_exist(self):
        self.popupate_database()
        response = self.client.delete('/todo/unknown_task', content_type='application/json')
        self.assert404(response)