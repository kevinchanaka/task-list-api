from api.models import Model
from typing import List


class MockDatabase:
    def __init__(self):
        self.data_list: List[Model] = []

    @staticmethod
    def __match__(obj: Model, filter):
        for k, v in filter.items():
            obj_val = getattr(obj, k, None)
            if obj_val and obj_val == v:
                continue
            else:
                return False
        return True

    def list(self, **filter):
        return [x for x in self.data_list if self.__match__(x, filter)]

    def get(self, **filter):
        output = self.list(**filter)
        if len(output) == 0:
            return None
        return output[0]

    def add(self, obj: Model):
        self.data_list.append(obj)
        return True

    def delete(self, **filter):
        obj_to_del = self.get(**filter)
        if obj_to_del is None:
            return False
        self.data_list = [x for x in self.data_list if not self.__match__(x, filter)]
        return True

    def update(self, obj: Model, **filter):
        for i in range(0, len(self.data_list)):
            if self.__match__(self.data_list[i], filter):
                self.data_list[i] = obj
                return True
        return False
