"""
Adding PayrollSystem and ProductivitySystem class here rather than creating
separating module for the sake of simplicity and understanding.
"""


class ProductivitySystem:
    def track(self, employees, hours):
        print("Tracking Employee Productivity")
        print("==============================")
        for employee in employees:
            employee.work(hours)
        print("")


class PayrollSystem:
    def calculate_payroll(self, employees):
        print("Calculating Payroll")
        print("===================")
        for employee in employees:
            print(f"Payroll for: {employee.id} - {employee.name}")
            print(f"- Check amount: {employee.calculate_payroll()}")
            print("")


class Employee:
    """
    Base class for every employee type
    """

    def __init__(self, id, name):
        self.id = id
        self.name = name


class SalaryEmployee(Employee):
    """
    Employee which have fixed salary. Get paid every week
    """

    def __init__(self, id, name, weekly_salary):
        super().__init__(id, name)
        self.weekly_salary = weekly_salary

    def calculate_payroll(self):
        return self.weekly_salary


class HourlyEmployee(Employee):
    """
    Employee which gets paid based on hours worked.
    """

    def __init__(self, id, name, hours_worked, hourly_rate):
        super().__init__(id, name)
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate

    def calculate_payroll(self):
        return self.hours_worked * self.hourly_rate


class Secretary(SalaryEmployee):
    def work(self, hours):
        print(f"{self.name} expends {hours} hours doing office paperwork.")


"""
Deriving from multiple base classes.
"""


class TemporarySecretaryOne(Secretary, HourlyEmployee):
    pass


class TemporarySecretaryTwo(HourlyEmployee, Secretary):
    pass


class TemporarySecretaryThree(HourlyEmployee, Secretary):
    def __init__(self, id, name, hours_worked, hourly_rate):
        super().__init__(id, name, hours_worked, hourly_rate)


class TemporarySecretaryByPassInit(Secretary, HourlyEmployee):
    """
    Effectively skipping Secretary and SalaryEmployee in the MRO
    when initializing an object.
    """

    def __init__(self, id, name, hours_worked, hourly_rate):
        HourlyEmployee.__init__(self, id, name, hours_worked, hourly_rate)


class TemporarySecretaryByPassInitPayroll(Secretary, HourlyEmployee):
    """
    Effectively skipping Secretary and SalaryEmployee in the MRO
    when initializing an object.
    """

    def __init__(self, id, name, hours_worked, hourly_rate):
        HourlyEmployee.__init__(self, id, name, hours_worked, hourly_rate)

    def calculate_payroll(self):
        return HourlyEmployee.calculate_payroll(self)


if __name__ == "__main__":
    # temporary_secretary = TemporarySecretaryOne(5, "Robin Williams", 40, 9)
    """
    Will raise a TypeError
    SalaryEmployee.__init__() takes 4 positional arguments but 5 were given
    Because TemporarySecretaryOne is derived first from Secretary and then
    from HourlyEmployee, so the interpreter is trying to use
    Secretary.__init__() to initialize the object.
    """

    # temporary_secretary = TemporarySecretaryTwo(5, "Robin Williams", 40, 9)
    """
    Now it seems that we’re missing a weekly_salary parameter, which is
    necessary to initialize Secretary.
    """

    # temporary_secretary = TemporarySecretaryThree(5, "Robin Williams", 40, 9)
    """
    This will not work either
    """

    # Checking MRO ( method resolution operator )
    print("===== By passing init method MRO ======")
    print(TemporarySecretaryByPassInit.__mro__)

    # temporary_secretary = TemporarySecretaryByPassInit(5, "Robin Williams", 40, 9)
    """
    This will not work while calculate_payroll.
    """

    print("\n===== By passing init and payroll method MRO ======")
    print(TemporarySecretaryByPassInitPayroll.__mro__)
    print("\n")
    temporary_secretary = TemporarySecretaryByPassInitPayroll(
        5, "Robin Williams", 40, 9
    )
    """
    works as expected because we’re forcing the method resolution
    order by explicitly telling the interpreter which method we want to use.
    """

    company_employees = [
        temporary_secretary,
    ]

    productivity_system = ProductivitySystem()
    productivity_system.track(company_employees, 40)

    payroll_system = PayrollSystem()
    payroll_system.calculate_payroll(company_employees)

    print(
        """
        There is an inherent diamond problem using this class design.
    """
    )

    print("          Employee         ")
    print("         /        \\       ")
    print(" SalaryEmployee     HourlyEmployee")
    print("    |                /")
    print("   Secretary        /")
    print("    \\             /")
    print(" TemporarySecretaryByPassInitPayroll")
