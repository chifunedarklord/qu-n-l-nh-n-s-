# -*- coding: utf-8 -*-
def format_currency(amount):
    """Format số tiền theo định dạng VND"""
    return f"{amount:,.0f} VNĐ"


def format_employee_info(employee):
    """Format thông tin nhân viên"""
    lines = [
        f"  ID         : {employee.employee_id}",
        f"  Họ tên     : {employee.name}",
        f"  Tuổi       : {employee.age}",
        f"  Email      : {employee.email}",
        f"  Phòng ban  : {employee.department}",
        f"  Chức vụ    : {employee.get_role()}",
        f"  Lương CB   : {format_currency(employee.base_salary)}",
        f"  Lương thực : {format_currency(employee.calculate_salary())}",
        f"  Hiệu suất  : {employee.performance_score}/10",
        f"  Dự án      : {', '.join(employee.projects) if employee.projects else 'Chưa có'}",
    ]
    return "\n".join(lines)


def format_separator(char="=", length=65):
    return char * length


def format_title(title, char="=", length=65):
    lines = [
        format_separator(char, length),
        title.center(length),
        format_separator(char, length),
    ]
    return "\n".join(lines)