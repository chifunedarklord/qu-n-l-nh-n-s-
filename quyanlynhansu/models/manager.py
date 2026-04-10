# -*- coding: utf-8 -*-
from models.employee import Employee


class Manager(Employee):
    """Class Manager kế thừa Employee
    Lương = base_salary * 1.5 + bonus
    """

    SALARY_MULTIPLIER = 1.5
    BONUS = 5_000_000

    def __init__(self, employee_id, name, age, email, department, base_salary, team_size=0):
        super().__init__(employee_id, name, age, email, department, base_salary)
        self.team_size = team_size

    def calculate_salary(self):
        """Lương Manager = base * 1.5 + 5,000,000 bonus"""
        return self.base_salary * self.SALARY_MULTIPLIER + self.BONUS

    def get_role(self):
        return "Manager"

    def __str__(self):
        base = super().__str__()
        return f"{base} | Nhóm: {self.team_size} người"