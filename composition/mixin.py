import json
from pprint import pprint


class JSONMixin:
    def to_json(self):
        print(json.dumps(self.to_dict()))


class DictMixin:
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, attributes):
        result = {}
        for key, val in attributes.items():
            result[key] = self._traverse(key, val)
        return val

    def _traverse(self, key, value):
        if isinstance(value, DictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, v) for v in value]
        elif hasattr(value, "__dict__"):
            return self._traverse_dict(value.__dict__)
        else:
            return value


class Person:
    def __init__(self, name):
        self.name = name


class Employee(DictMixin, JSONMixin, Person):
    def __init__(self, name, skills, dependents):
        super().__init__(name)
        self.skills = skills
        self.dependents = dependents


if __name__ == "__main__":
    e = Employee(
        name="Ayush",
        skills=["Python Programming" "Project Management"],
        dependents={"wife": "Jane", "children": ["Alice", "Bob"]},
    )

    pprint(e.to_dict())
    e.to_json()
