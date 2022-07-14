from unittest import TestCase
from tests.integration import clean_up_db_table, create_test_client_auth
from tests.data import test_task_no_id as test_task

PATH = "/api/v1/tasks"


class TestTask(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_test_client_auth()

    def setUp(self):
        res = self.app.post(f"{PATH}/", json=test_task)
        self.assertEqual(res.status_code, 200)
        self.task = res.get_json()["task"]
        self.assertIsInstance(self.task, dict)

    def tearDown(self):
        clean_up_db_table("tasks")

    def test_01_get_task(self):
        task_id = self.task["id"]
        res = self.app.get(f"{PATH}/{task_id}")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json()["task"], dict)

    def test_02_list_tasks(self):
        res = self.app.get(f"{PATH}/")
        self.assertEqual(res.status_code, 200)
        tasks = res.get_json()["tasks"]
        self.assertIsInstance(tasks, list)
        self.assertIsInstance(tasks[0], dict)

    def test_03_update_task(self):
        task_id = self.task["id"]
        modified_task = {"name": "task2", "description": "desc2"}
        res = self.app.put(f"{PATH}/{task_id}", json=modified_task)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json()["task"], dict)

    def test_04_delete_task(self):
        task_id = self.task["id"]
        res = self.app.delete(f"{PATH}/{task_id}")
        self.assertEqual(res.status_code, 200)
