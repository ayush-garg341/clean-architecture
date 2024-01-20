"""
In the previous implementation we saw how our system fails.
Here is a fix for that.
"""

from abc import ABC, abstractmethod


class Employee(ABC):
    """
    Making Employee an abstract base class.
    """

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def class_name(self):
        return "This is Abstract base class\n"

    @abstractmethod
    def calculate_payroll(self):
        pass


class SalaryEmployee(Employee):
    """
    Employee which have fixed salary. Get paid every week
    """

    def __init__(self, id, name, weekly_salary):
        super().__init__(id, name)
        self.weekly_salary = weekly_salary

    def calculate_payroll(self):
        return self.weekly_salary


if __name__ == "__main__":
    print(
        """
    How does making Employee an abstract base class helps us ?
    This change has two side effects.
        - We're telling users of the module that objects of type Employee
          can’t be created.
        - We're telling other developers working on this module that if they
          derive from Employee, then they must override the
          .calculate_payroll() abstract method.
    """
    )
    # employee = SalaryEmployee(1, "Abstract", 5000)
    # print(employee.class_name())

    employee = Employee(2, "Random")
