import json
from freezegun import freeze_time

from tests.sqlite_config import SQLiteConfig
from tests.common import parametrized

from todo_list.app import TaskModel


class TestGetTask(SQLiteConfig):
    def popupate_database(self):
        request_data = [
            {
                "task_id": "test_1", "deadline": "2022-11-29", "text": "smth important 1"
            },
            {
                "task_id": "test_2", "deadline": "2022-12-10", "text": "smth important 2"
            },
            {
                "task_id": "test_3", "deadline": "2023-01-01", "text": "smth important 3"
            },
            {
                "task_id": "test_4", "deadline": "2022-11-10", "text": "smth important 4", "is_done": True
            },
            {
                "task_id": "test_5", "deadline": "2022-12-01", "text": "smth important 5"
            },
        ]
        for todo in request_data:
            response = self.client.post('/todo', data=json.dumps(todo), content_type='application/json')
            self.assertStatus(response, 201)

        # check if all records have been populated
        self.assertEqual(5, TaskModel.query.count())

    def test_get_all_tasks(self):
        self.popupate_database()
        expected_response = [
            {
                "task_id": "test_1", "deadline": "2022-11-29", "text": "smth important 1", "is_done": False
            },
            {
                "task_id": "test_2", "deadline": "2022-12-10", "text": "smth important 2", "is_done": False
            },
            {
                "task_id": "test_3", "deadline": "2023-01-01", "text": "smth important 3", "is_done": False
            },
            {
                "task_id": "test_4", "deadline": "2022-11-10", "text": "smth important 4", "is_done": True
            },
            {
                "task_id": "test_5", "deadline": "2022-12-01", "text": "smth important 5", "is_done": False
            },
        ]

        response = self.client.get('/todos', content_type='application/json')
        response_body = response.json
        self.assert200(response, response.status)
        self.assertIsInstance(response_body, list)
        self.assertEqual(5, len(response_body), 'Incorrect todo count.')
        self.assertEqual(expected_response, response_body)

    def test_filter_by_date_range(self):
        self.popupate_database()
        expected_response = [
            {
                "task_id": "test_3", "deadline": "2023-01-01", "text": "smth important 3", "is_done": False
            }
        ]
        response = self.client.get('/todos?date_from=2022-12-31&date_to=2023-01-10', content_type='application/json')
        response_body = response.json
        self.assert200(response, response.status)
        self.assertEqual(expected_response, response_body)

    @freeze_time("2022-12-01")
    def test_filter_by_today_date(self):
        self.popupate_database()
        expected_response = [
            {
                "task_id": "test_4", "deadline": "2022-11-10", "text": "smth important 4", "is_done": True
            }
        ]
        response = self.client.get('/todos?date_to=now&is_done=True', content_type='application/json')
        response_body = response.json
        self.assert200(response, response.status)
        self.assertEqual(expected_response, response_body)

    @freeze_time("2022-12-01")
    def test_filter_most_urgent_todo(self):
        self.popupate_database()
        expected_response = [
            {
                "task_id": "test_5", "deadline": "2022-12-01", "text": "smth important 5", "is_done": False
            }
        ]
        response = self.client.get('/todos?date_from=now&count=1&sort_by=urgency',
                                   content_type='application/json')
        response_body = response.json
        self.assert200(response, response.status)
        self.assertEqual(expected_response, response_body)

        response = self.client.get('/most-urgent',
                                   content_type='application/json')
        self.assertStatus(response, 302)
        self.assertIn('/todos?date_from=now&count=1&sort_by=urgency', response.location)

    @freeze_time("2022-12-01")
    def test_filter_after_deadline_todo(self):
        self.popupate_database()
        expected_response = [
            {
                "task_id": "test_1", "deadline": "2022-11-29", "text": "smth important 1", "is_done": False
            },
            {
                "task_id": "test_5", "deadline": "2022-12-01", "text": "smth important 5", "is_done": False
            }
        ]
        response = self.client.get('/todos?date_to=now&is_done=False',
                                   content_type='application/json')
        response_body = response.json
        self.assert200(response, response.status)
        self.assertEqual(expected_response, response_body)

    @parametrized([{"date_from": "today", "date_to": "2022-12-01", "status_code": 400, "message":""}])
    def test_invalid_parameters(self, date_from, date_to):
        pass
