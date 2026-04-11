# -*- coding: utf-8 -*-
import random
from models.manager import Manager
from models.developer import Developer
from models.intern import Intern
from exceptions.employee_exceptions import (
    EmployeeNotFoundError, DuplicateEmployeeError, ProjectAllocationError
)

MAX_PROJECTS = 5


class Company:
    """Class Company quản lý danh sách nhân viên"""

    def __init__(self, name="Công ty ABC"):
        self.name = name
        self._employees = {}  # {employee_id: Employee}

    # ─── Helpers ──────────────────────────────────────────────────
    def _generate_id(self, prefix="NV"):
        """Tự sinh ID mới không trùng"""
        while True:
            new_id = f"{prefix}{random.randint(1000, 9999)}"
            if new_id not in self._employees:
                return new_id

    def _get_or_raise(self, employee_id):
        if employee_id not in self._employees:
            raise EmployeeNotFoundError(employee_id)
        return self._employees[employee_id]

    @property
    def employees(self):
        return list(self._employees.values())

    # ─── 1. Thêm nhân viên ───────────────────────────────────────
    def add_employee(self, employee):
        """Thêm nhân viên, tự sinh ID nếu trùng"""
        if employee.employee_id in self._employees:
            new_id = self._generate_id()
            print(f"  ⚠  ID '{employee.employee_id}' đã tồn tại → tự động đổi thành '{new_id}'")
            employee.employee_id = new_id
        self._employees[employee.employee_id] = employee
        return employee

    # ─── 2. Hiển thị ─────────────────────────────────────────────
    def get_all_employees(self):
        if not self._employees:
            raise IndexError("Chưa có dữ liệu nhân viên")
        return self.employees

    def get_employees_by_role(self, role):
        """Lọc theo loại: Manager / Developer / Intern"""
        result = [e for e in self.employees if e.get_role().lower() == role.lower()]
        if not result:
            raise IndexError(f"Không có nhân viên nào thuộc loại '{role}'")
        return result

    def get_employees_by_performance(self):
        """Sắp xếp theo hiệu suất giảm dần"""
        if not self._employees:
            raise IndexError("Chưa có dữ liệu nhân viên")
        return sorted(self.employees, key=lambda e: e.performance_score, reverse=True)

    # ─── 3. Tìm kiếm ─────────────────────────────────────────────
    def find_by_id(self, employee_id):
        return self._get_or_raise(employee_id)

    def find_by_name(self, name):
        result = [e for e in self.employees if name.lower() in e.name.lower()]
        if not result:
            raise EmployeeNotFoundError(f"(tên: {name})")
        return result

    def find_by_language(self, language):
        """Tìm Developer theo ngôn ngữ lập trình"""
        result = [e for e in self.employees
                  if isinstance(e, Developer) and
                  language.lower() in e.programming_language.lower()]
        if not result:
            raise EmployeeNotFoundError(f"(ngôn ngữ: {language})")
        return result

    # ─── 4. Lương ────────────────────────────────────────────────
    # (delegated to Payroll service, but company provides data)

    # ─── 5. Quản lý dự án ────────────────────────────────────────
    def assign_project(self, employee_id, project_name):
        emp = self._get_or_raise(employee_id)
        if len(emp.projects) >= MAX_PROJECTS:
            raise ProjectAllocationError(
                f"Nhân viên {emp.name} đã có {MAX_PROJECTS} dự án, không thể thêm"
            )
        emp.add_project(project_name)

    def remove_from_project(self, employee_id, project_name):
        emp = self._get_or_raise(employee_id)
        if not emp.remove_project(project_name):
            raise ValueError(f"Nhân viên không tham gia dự án '{project_name}'")

    def get_employee_projects(self, employee_id):
        emp = self._get_or_raise(employee_id)
        return emp.projects

    # ─── 6. Hiệu suất ────────────────────────────────────────────
    def update_performance(self, employee_id, score):
        emp = self._get_or_raise(employee_id)
        emp.update_performance(score)

    def get_excellent_employees(self):
        result = [e for e in self.employees if e.performance_score > 8]
        if not result:
            raise IndexError("Không có nhân viên xuất sắc (điểm > 8)")
        return result

    def get_needs_improvement(self):
        result = [e for e in self.employees if e.performance_score < 5]
        if not result:
            raise IndexError("Không có nhân viên cần cải thiện (điểm < 5)")
        return result

    # ─── 7. Quản lý nhân sự ──────────────────────────────────────
    def remove_employee(self, employee_id):
        emp = self._get_or_raise(employee_id)
        del self._employees[employee_id]
        return emp

    def raise_salary(self, employee_id, amount):
        emp = self._get_or_raise(employee_id)
        emp.base_salary += amount

    def promote(self, employee_id):
        """Thăng chức: Intern→Developer, Developer→Manager"""
        emp = self._get_or_raise(employee_id)
        role = emp.get_role()

        if role == "Intern":
            new_emp = Developer(
                emp.employee_id, emp.name, emp.age, emp.email,
                emp.department, emp.base_salary
            )
        elif role == "Developer":
            new_emp = Manager(
                emp.employee_id, emp.name, emp.age, emp.email,
                emp.department, emp.base_salary
            )
        else:
            raise ValueError(f"Manager không thể thăng chức thêm")

        new_emp.performance_score = emp.performance_score
        new_emp.projects = emp.projects.copy()
        self._employees[employee_id] = new_emp
        return role, new_emp.get_role(), new_emp

    # ─── 5b. Thống kê dự án (mới) ────────────────────────────────
    def get_top_most_projects(self, top_n=10):
        """Top N nhân viên tham gia nhiều dự án nhất"""
        if not self._employees:
            raise IndexError("Chưa có dữ liệu nhân viên")
        sorted_emps = sorted(self.employees, key=lambda e: len(e.projects), reverse=True)
        return sorted_emps[:top_n]

    def get_top_least_projects(self, top_n=10):
        """Top N nhân viên tham gia ít dự án nhất"""
        if not self._employees:
            raise IndexError("Chưa có dữ liệu nhân viên")
        sorted_emps = sorted(self.employees, key=lambda e: len(e.projects))
        return sorted_emps[:top_n]

    def get_employees_in_project(self, project_name):
        """Danh sách thành viên tham gia 1 dự án cụ thể và chức vụ"""
        result = [e for e in self.employees if project_name in e.projects]
        if not result:
            raise IndexError(f"Không có nhân viên nào tham gia dự án '{project_name}'")
        return result

    # ─── 7b. Cắt giảm nhân sự hàng loạt (mới) ───────────────────
    def bulk_layoff(self, employee_ids):
        """Cho nghỉ việc nhiều nhân viên cùng lúc, trả về danh sách đã xóa"""
        removed = []
        errors  = []
        for eid in employee_ids:
            try:
                emp = self.remove_employee(eid)
                removed.append(emp)
            except EmployeeNotFoundError as e:
                errors.append(str(e))
        return removed, errors