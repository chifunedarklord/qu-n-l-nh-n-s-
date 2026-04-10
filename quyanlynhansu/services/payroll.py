# -*- coding: utf-8 -*-


class Payroll:
    """Hàm tính lương và thống kê"""

    @staticmethod
    def calculate_employee_salary(employee):
        """Tính lương cho một nhân viên"""
        return employee.calculate_salary()

    @staticmethod
    def calculate_total_salary(employees):
        """Tính tổng lương công ty"""
        return sum(emp.calculate_salary() for emp in employees)

    @staticmethod
    def get_top_salary(employees, top_n=3):
        """Lấy top N nhân viên lương cao nhất"""
        sorted_employees = sorted(employees, key=lambda e: e.calculate_salary(), reverse=True)
        return sorted_employees[:top_n]

    @staticmethod
    def get_salary_by_department(employees):
        """Tổng lương theo phòng ban"""
        dept_salary = {}
        for emp in employees:
            dept = emp.department
            if dept not in dept_salary:
                dept_salary[dept] = 0
            dept_salary[dept] += emp.calculate_salary()
        return dept_salary

    @staticmethod
    def count_by_role(employees):
        """Đếm số lượng nhân viên theo loại"""
        counts = {}
        for emp in employees:
            role = emp.get_role()
            counts[role] = counts.get(role, 0) + 1
        return counts

    @staticmethod
    def avg_projects_per_employee(employees):
        """Số dự án trung bình trên mỗi nhân viên"""
        if not employees:
            return 0
        total_projects = sum(len(emp.projects) for emp in employees)
        return total_projects / len(employees)