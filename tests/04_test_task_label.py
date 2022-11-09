from tests import BaseTestClass
from tests.data import test_label, test_task

LABEL_PATH = "/api/v1/labels"
TASK_PATH = "/api/v1/tasks"


class TestTaskLabel(BaseTestClass):
    def assertLabel(self, label1, label2=test_label):
        self.assertEqual(label1["name"], label2["name"])
        self.assertEqual(label1["colour"], label2["colour"])

    def assertTask(self, task1, task2=test_task):
        self.assertEqual(task1["name"], task2["name"])
        self.assertEqual(task1["description"], task2["description"])

    def setUp(self):
        super().setUp()
        res = self.client.post(f"{LABEL_PATH}/", json=test_label)
        self.label = res.get_json()["label"]
        res = self.client.post(f"{TASK_PATH}/", json=test_task)
        self.task = res.get_json()["task"]
        res = self.client.post(
            f'{TASK_PATH}/{self.task["id"]}/attach', json={"labels": [self.label["id"]]}
        )

    def test_task_label_01_get_tasks_with_label_info(self):
        tasks = self.client.get(f"{TASK_PATH}/").get_json()["tasks"]
        self.assertIsInstance(tasks, list)
        self.assertIsInstance(tasks[0]["labels"], list)
        self.assertLabel(tasks[0]["labels"][0])

    def test_task_label_02_get_task_with_label_info(self):
        task = self.client.get(f'{TASK_PATH}/{self.task["id"]}').get_json()["task"]
        self.assertIsInstance(task["labels"], list)
        self.assertLabel(task["labels"][0])

    def test_task_label_03_detach_labels_from_task(self):
        res = self.client.post(
            f'{TASK_PATH}/{self.task["id"]}/detach', json={"labels": [self.label["id"]]}
        )
        self.assertEqual(res.status_code, 200)
        res = self.client.get(f'{TASK_PATH}/{self.task["id"]}').get_json()
        self.assertEqual(res["task"]["labels"], [])

    def test_task_label_04_update_label_task(self):
        label_id = self.label["id"]
        modified_label = {"name": "label2", "colour": "#ababab"}
        self.client.put(f"{LABEL_PATH}/{label_id}", json=modified_label)
        task = self.client.get(f'{TASK_PATH}/{self.task["id"]}').get_json()["task"]
        self.assertLabel(modified_label, task["labels"][0])

    def test_task_label_05_delete_label_task(self):
        label_id = self.label["id"]
        self.client.delete(f"{LABEL_PATH}/{label_id}")
        task = self.client.get(f'{TASK_PATH}/{self.task["id"]}').get_json()["task"]
        self.assertEqual(task["labels"], [])
