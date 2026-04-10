# -*- coding: utf-8 -*-
import re
from exceptions.employee_exceptions import InvalidAgeError, InvalidSalaryError


def validate_age(age):
    """Kiểm tra tuổi hợp lệ (18-65)"""
    if not isinstance(age, int) or age < 18 or age > 65:
        raise InvalidAgeError(f"Tuổi phải từ 18 đến 65. Giá trị nhập: {age}")
    return True


def validate_salary(salary):
    """Kiểm tra lương hợp lệ (> 0)"""
    if not isinstance(salary, (int, float)) or salary <= 0:
        raise InvalidSalaryError(f"Lương phải lớn hơn 0. Giá trị nhập: {salary}")
    return True


def validate_email(email):
    """Kiểm tra định dạng email"""
    if not email or '@' not in email:
        raise ValueError(f"Email không hợp lệ: '{email}'. Email phải chứa ký tự '@'")
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email):
        raise ValueError(f"Email không đúng định dạng: '{email}'")
    return True


def validate_performance_score(score):
    """Kiểm tra điểm hiệu suất (0-10)"""
    if not isinstance(score, (int, float)) or score < 0 or score > 10:
        raise ValueError(f"Điểm hiệu suất phải từ 0 đến 10. Giá trị nhập: {score}")
    return True