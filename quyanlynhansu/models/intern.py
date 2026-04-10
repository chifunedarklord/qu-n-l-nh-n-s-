# -*- coding: utf-8 -*-
from models.employee import Employee


class Intern(Employee):
    """Class Intern kế thừa Employee
    Lương = base_salary * 0.7
    """

    SALARY_MULTIPLIER = 0.7

    def __init__(self, employee_id, name, age, email, department, base_salary, school=""):
        super().__init__(employee_id, name, age, email, department, base_salary)
        self.school = school

    def calculate_salary(self):
        """Lương Intern = base * 0.7"""
        return self.base_salary * self.SALARY_MULTIPLIER

    def get_role(self):
        return "Intern"

    def __str__(self):
        base = super().__str__()
        return f"{base} | Trường: {self.school}"