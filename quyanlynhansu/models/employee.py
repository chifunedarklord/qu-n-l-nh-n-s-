# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from utils.validators import validate_age, validate_salary, validate_email
from utils.formatters import format_currency


class Employee(ABC):
    """Class Employee trừu tượng (abstract/base)"""

    def __init__(self, employee_id, name, age, email, department, base_salary):
        validate_age(age)
        validate_salary(base_salary)
        validate_email(email)

        self.employee_id = employee_id
        self.name = name
        self.age = age
        self.email = email
        self.department = department
        self.base_salary = base_salary
        self.performance_score = 0.0
        self.projects = []

    @abstractmethod
    def calculate_salary(self):
        """Tính lương thực nhận (abstract method)"""
        pass

    @abstractmethod
    def get_role(self):
        """Lấy chức vụ của nhân viên"""
        pass

    def update_performance(self, score):
        """Cập nhật điểm hiệu suất"""
        self.performance_score = score

    def add_project(self, project_name):
        """Thêm dự án"""
        self.projects.append(project_name)

    def remove_project(self, project_name):
        """Xóa dự án"""
        if project_name in self.projects:
            self.projects.remove(project_name)
            return True
        return False

    def __str__(self):
        return (f"[{self.get_role()}] {self.employee_id} - {self.name} | "
                f"Phòng: {self.department} | Lương: {format_currency(self.calculate_salary())} | "
                f"Hiệu suất: {self.performance_score}/10")