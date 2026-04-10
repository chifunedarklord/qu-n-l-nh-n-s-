# -*- coding: utf-8 -*-
from models.employee import Employee


class Developer(Employee):
    """Class Developer kế thừa Employee
    Lương = base_salary * 1.3 + project_bonus
    """

    SALARY_MULTIPLIER = 1.3
    PROJECT_BONUS = 2_000_000

    def __init__(self, employee_id, name, age, email, department, base_salary, programming_language="Python"):
        super().__init__(employee_id, name, age, email, department, base_salary)
        self.programming_language = programming_language

    def calculate_salary(self):
        """Lương Developer = base * 1.3 + 2,000,000 * số dự án"""
        project_bonus = self.PROJECT_BONUS * len(self.projects)
        return self.base_salary * self.SALARY_MULTIPLIER + project_bonus

    def get_role(self):
        return "Developer"

    def __str__(self):
        base = super().__str__()
        return f"{base} | Ngôn ngữ: {self.programming_language}"