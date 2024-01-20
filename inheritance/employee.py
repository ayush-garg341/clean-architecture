# Implementing payroll system with productivity system
"""
Managers        :- They’re salaried employees and make more money.
Secretaries    :- They do all the paperwork for managers.
                - They’re also salaried employees but make less money.
Sales employees:- They have a salary, but they also get commissions for sales.
Factory workers:- They manufacture the products for the company. Paid by hour
"""

print("======================== version v2 ======================")


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


class ComissionEmployee(SalaryEmployee):
    """
    Employee who gets fixed weekly salary but commission also.
    """

    def __init__(self, id, name, weekly_salary, commission):
        super().__init__(id, name, weekly_salary)
        self.commission = commission

    def calculate_payroll(self):
        """
        Could have access weekly_salary property directly from SalaryEmployee,
        but if super/base class calculate_payroll changed,
        we have to make change in derive class too,
        so it's better to rely on base class calculate_payroll.
        """
        fixed = super().calculate_payroll()
        return fixed + self.commission


class Manager(SalaryEmployee):
    def work(self, hours):
        print(f"{self.name} screams and yells for {hours} hours.")


class Secretary(SalaryEmployee):
    def work(self, hours):
        print(f"{self.name} expends {hours} hours doing office paperwork.")


class SalesPerson(ComissionEmployee):
    def work(self, hours):
        print(f"{self.name} expends {hours} hours on the phone.")


class FactoryWorker(HourlyEmployee):
    def work(self, hours):
        print(f"{self.name} manufactures gadgets for {hours} hours.")


if __name__ == "__main__":
    salary_employee = SalaryEmployee(1, "John Smith", 1500)
    hourly_employee = HourlyEmployee(2, "Jane Doe", 40, 15)
    commission_employee = ComissionEmployee(3, "Kevin Bacon", 1000, 250)

    payroll_system = PayrollSystem()
    payroll_system.calculate_payroll(
        [salary_employee, hourly_employee, commission_employee]
    )

    print(
        """
    But this system has an inherent issue, whats that ?
    If we pass our payroll system an instance of Employee class directly,
    it will break because Employee does not have calculate_payroll() method.
    """
    )

    employee = Employee(1, "Invalid")
    payroll_system = PayrollSystem()
    payroll_system.calculate_payroll([employee])
