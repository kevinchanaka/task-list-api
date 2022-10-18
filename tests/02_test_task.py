from tests import BaseTestClass
from tests.data import test_task

PATH = "/api/v1/tasks"


class TestTask(BaseTestClass):
    def assertTask(self, task1, task2=test_task):
        self.assertEqual(task1["name"], task2["name"])
        self.assertEqual(task1["description"], task2["description"])

    def setUp(self):
        super().setUp()
        res = self.client.post(f"{PATH}/", json=test_task)
        self.assertEqual(res.status_code, 200)
        self.task = res.get_json()["task"]
        self.assertTask(self.task)

    def test_task_01_get_task(self):
        task_id = self.task["id"]
        res = self.client.get(f"{PATH}/{task_id}")
        self.assertEqual(res.status_code, 200)
        self.assertTask(res.get_json()["task"])

    def test_task_02_list_tasks(self):
        res = self.client.get(f"{PATH}/")
        self.assertEqual(res.status_code, 200)
        tasks = res.get_json()["tasks"]
        self.assertIsInstance(tasks, list)
        self.assertTask(tasks[0])

    def test_task_03_update_task(self):
        task_id = self.task["id"]
        modified_task = {"name": "task2", "description": "desc2", "completed": True}
        res = self.client.put(f"{PATH}/{task_id}", json=modified_task)
        self.assertEqual(res.status_code, 200)
        new_task = self.client.get(f"{PATH}/{task_id}").get_json()["task"]
        self.assertTask(modified_task, new_task)

    def test_task_04_delete_task(self):
        task_id = self.task["id"]
        res = self.client.delete(f"{PATH}/{task_id}")
        self.assertEqual(res.status_code, 200)
        res = self.client.get(f"{PATH}/{task_id}")
        self.assertEqual(res.status_code, 400)
