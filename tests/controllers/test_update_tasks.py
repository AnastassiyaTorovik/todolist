import json

from tests.sqlite_config import SQLiteConfig

from todo_list.app import TaskModel


class TestGetTask(SQLiteConfig):
    def popupate_database(self):
        request_data = [
            {
                "task_id": "test_1", "deadline": "2022-11-29", "text": "smth important 1"
            },
            {
                "task_id": "test_2", "deadline": "2022-11-10", "text": "smth important 2", "is_done": True
            }
        ]
        for todo in request_data:
            response = self.client.post('/todo', data=json.dumps(todo), content_type='application/json')
            self.assertStatus(response, 201)

        # check if all records have been populated
        self.assertEqual(2, TaskModel.query.count())

    def test_put_status_done(self):
        self.popupate_database()
        response = self.client.put('/test_1/set-done', content_type='application/json')
        self.assert200(response)

        # check if status updated
        response = self.client.get('todos?is_done=True', content_type='application/json')
        self.assert200(response)
        self.assertEqual(2, len(response.json))

    def test_put_status_not_done(self):
        self.popupate_database()
        response = self.client.put('/test_2/set-not-done', content_type='application/json')
        self.assert200(response)

        # check if status updated
        response = self.client.get('todos?is_done=False', content_type='application/json')
        self.assert200(response)
        self.assertEqual(2, len(response.json))

    def test_update_task_not_exist(self):
        self.popupate_database()
        response = self.client.put('/unknown_task/set-done', content_type='application/json')
        self.assert404(response)

        response = self.client.put('/unknown_task/set-not-done', content_type='application/json')
        self.assert404(response)


