from unittest import TestCase, mock
from tests.unit import MockDatabase
from tests.data import test_task
from api.services import task_service
from api.models import Task
from api.exceptions import InvalidUsageError

task_obj = Task.deserialise(**test_task)


class TestTaskService(TestCase):
    def setUp(self):
        self.task_db_mock = mock.patch(
            "api.services.task.task_db", new_callable=MockDatabase
        )

        self.task_db = self.task_db_mock.start()

    def tearDown(self):
        self.task_db_mock.stop()

    def assert_task(self, data):
        self.assertIn("id", data)
        self.assertIn("name", data)
        self.assertIn("description", data)
        self.assertNotIn("user_id", data)

    def test_01_create_task(self):
        ret = task_service.create_task(task_obj)
        self.assertIn("task", ret)
        self.assert_task(ret["task"])

    def test_02_get_task(self):
        task_service.create_task(task_obj)
        ret = task_service.get_task(task_obj.user_id, task_obj.id)
        self.assertIn("task", ret)
        self.assert_task(ret["task"])

    def test_03_list_tasks(self):
        task_service.create_task(task_obj)
        tasks = task_service.list_tasks(user_id=task_obj.user_id)
        task_list = tasks["tasks"]
        self.assertIsInstance(task_list, list)
        self.assertEqual(len(task_list), 1)
        self.assert_task(task_list[0])

    def test_03_update_task(self):
        task_service.create_task(task_obj)
        new_name = "task2"
        task_obj.name = new_name
        ret = task_service.update_task(task_obj)
        self.assertEqual(new_name, ret["task"]["name"])

    def test_04_delete_task(self):
        task_service.create_task(task_obj)
        task_service.delete_task(user_id=task_obj.user_id, task_id=task_obj.id)
        self.assertRaises(
            InvalidUsageError, task_service.get_task, task_obj.user_id, task_obj.id
        )
