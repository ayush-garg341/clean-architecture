"""
Final design of our classes to avoid diamond problem
"""

print(" =====================  version v3 ================ ")


# Productivity module
class ProductivitySystem:
    def track(self, employees, hours):
        print("Tracking Employee Productivity v3")
        print("==============================")
        for employee in employees:
            result = employee.work(hours)
            print(f"{employee.name}: {result}")
        print("")


class ManagerRole:
    def work(self, hours):
        return f"screams and yells for {hours} hours."


class SecretaryRole:
    def work(self, hours):
        return f"expends {hours} hours doing office paperwork."


class SalesRole:
    def work(self, hours):
        return f"expends {hours} hours on the phone."


class FactoryRole:
    def work(self, hours):
        return f"manufactures gadgets for {hours} hours."


# HR module.
class PayrollSystem:
    def calculate_payroll(self, employees):
        print("Calculating Payroll")
        print("===================")
        for employee in employees:
            print(f"Payroll for: {employee.id} - {employee.name}")
            print(f"- Check amount: {employee.calculate_payroll()}")
            print("")


class SalaryPolicy:
    def __init__(self, weekly_salary):
        self.weekly_salary = weekly_salary

    def calculate_payroll(self):
        return self.weekly_salary


class HourlyPolicy:
    def __init__(self, hours_worked, hourly_rate):
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate

    def calculate_payroll(self):
        return self.hours_worked * self.hourly_rate


class CommissionPolicy(SalaryPolicy):
    def __init__(self, weekly_salary, commission):
        super().__init__(weekly_salary)
        self.commission = commission

    def calculate_payroll(self):
        fixed = super().calculate_payroll()
        return fixed + self.commission


# Employee module
class Employee:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Manager(Employee, ManagerRole, SalaryPolicy):
    def __init__(self, id, name, weekly_salary):
        SalaryPolicy.__init__(self, weekly_salary)
        super().__init__(id, name)


class Secretary(Employee, SecretaryRole, SalaryPolicy):
    def __init__(self, id, name, weekly_salary):
        SalaryPolicy.__init__(self, weekly_salary)
        super().__init__(id, name)


class SalesPerson(Employee, SalesRole, CommissionPolicy):
    def __init__(self, id, name, weekly_salary, commission):
        CommissionPolicy.__init__(self, weekly_salary, commission)
        super().__init__(id, name)


class FactoryWorker(Employee, FactoryRole, HourlyPolicy):
    def __init__(self, id, name, hours_worked, hourly_rate):
        HourlyPolicy.__init__(self, hours_worked, hourly_rate)
        super().__init__(id, name)


class TemporarySecretary(Employee, SecretaryRole, HourlyPolicy):
    def __init__(self, id, name, hours_worked, hourly_rate):
        HourlyPolicy.__init__(self, hours_worked, hourly_rate)
        super().__init__(id, name)


if __name__ == "__main__":
    manager = Manager(1, "Mary Poppins", 3000)
    secretary = Secretary(2, "John Smith", 1500)
    sales_guy = SalesPerson(3, "Kevin Bacon", 1000, 250)
    factory_worker = FactoryWorker(4, "Jane Doe", 40, 15)
    temporary_secretary = TemporarySecretary(5, "Robin Williams", 40, 9)
    employees = [manager, secretary, sales_guy, factory_worker, temporary_secretary]

    productivity_system = ProductivitySystem()
    productivity_system.track(employees, 40)

    payroll_system = PayrollSystem()
    payroll_system.calculate_payroll(employees)
