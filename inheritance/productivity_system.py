"""
ProductivitySystem tracks productivity based on employee roles.
"""

from employee import *


class ProductivitySystem:
    def track(self, employees, hours):
        print("Tracking Employee Productivity")
        print("==============================")
        for employee in employees:
            employee.work(hours)
        print("")


"""
Adding PayrollSystem class here rather than creating separating module for
the sake of simplicity and understanding.
"""


class PayrollSystem:
    def calculate_payroll(self, employees):
        print("Calculating Payroll")
        print("===================")
        for employee in employees:
            print(f"Payroll for: {employee.id} - {employee.name}")
            print(f"- Check amount: {employee.calculate_payroll()}")
            print("")


if __name__ == "__main__":
    manager = Manager(1, "Mary Poppins", 3000)
    secretary = Secretary(2, "John Smith", 1500)
    sales_guy = SalesPerson(3, "Kevin Bacon", 1000, 250)
    factory_worker = FactoryWorker(4, "Jane Doe", 40, 15)
    employees = [
        manager,
        secretary,
        sales_guy,
        factory_worker,
    ]

    productivity_system = ProductivitySystem()
    productivity_system.track(employees, 40)

    payroll_system = PayrollSystem()
    payroll_system.calculate_payroll(employees)

    print(
        """
        Employee: Base Class
        SalaryEmployee, ComissionEmployee, HourlyEmployee:- inherit/extend from Employee base class
        Manager, Secretary:- inherits/extend SalaryEmployee class
        SalesPerson:- inherits/extend from ComissionEmployee class
        FactoryWorker:- inherits/extend from HourlyEmployee class
        """
    )
