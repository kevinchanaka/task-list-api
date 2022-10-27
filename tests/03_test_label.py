from tests import BaseTestClass
from tests.data import test_label

PATH = "/api/v1/labels"


class TestLabel(BaseTestClass):
    def assertLabel(self, label1, label2=test_label):
        self.assertEqual(label1["name"], label2["name"])
        self.assertEqual(label1["colour"], label2["colour"])

    def setUp(self):
        super().setUp()
        res = self.client.post(f"{PATH}/", json=test_label)
        self.assertEqual(res.status_code, 200)
        self.label = res.get_json()["label"]
        self.assertLabel(self.label)

    def test_label_01_get_label(self):
        label_id = self.label["id"]
        res = self.client.get(f"{PATH}/{label_id}")
        self.assertEqual(res.status_code, 200)
        self.assertLabel(res.get_json()["label"])

    def test_label_02_list_labels(self):
        res = self.client.get(f"{PATH}/")
        self.assertEqual(res.status_code, 200)
        labels = res.get_json()["labels"]
        self.assertIsInstance(labels, list)
        self.assertLabel(labels[0])

    def test_label_03_update_label(self):
        label_id = self.label["id"]
        modified_label = {"name": "label2", "colour": "#ababab"}
        res = self.client.put(f"{PATH}/{label_id}", json=modified_label)
        self.assertEqual(res.status_code, 200)
        new_label = self.client.get(f"{PATH}/{label_id}").get_json()["label"]
        self.assertLabel(modified_label, new_label)

    def test_label_04_delete_label(self):
        label_id = self.label["id"]
        res = self.client.delete(f"{PATH}/{label_id}")
        self.assertEqual(res.status_code, 200)
        res = self.client.get(f"{PATH}/{label_id}")
        self.assertEqual(res.status_code, 400)
