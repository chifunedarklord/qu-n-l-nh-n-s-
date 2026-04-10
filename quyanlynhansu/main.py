# -*- coding: utf-8 -*-
import sys
import os

# Fix encoding cho Windows terminal
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stdin  = io.TextIOWrapper(sys.stdin.buffer,  encoding='utf-8', errors='replace')

# Thêm thư mục gốc vào sys.path để import đúng
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.manager import Manager
from models.developer import Developer
from models.intern import Intern
from services.company import Company
from services.payroll import Payroll
from utils.formatters import (
    format_currency, format_employee_info,
    format_separator, format_title
)
from utils.validators import validate_age, validate_salary, validate_email, validate_performance_score
from exceptions.employee_exceptions import (
    EmployeeNotFoundError, InvalidAgeError, InvalidSalaryError,
    ProjectAllocationError, DuplicateEmployeeError
)

company = Company("Công ty ABC")


# ─── Input helpers ────────────────────────────────────────────────────────────

def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  ✗ Vui lòng nhập số nguyên hợp lệ!")


def input_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ✗ Vui lòng nhập số hợp lệ!")


def input_age(prompt):
    while True:
        try:
            age = input_int(prompt)
            validate_age(age)
            return age
        except InvalidAgeError as e:
            print(f"  ✗ {e}")


def input_salary(prompt):
    while True:
        try:
            sal = input_float(prompt)
            validate_salary(sal)
            return sal
        except InvalidSalaryError as e:
            print(f"  ✗ {e}")


def input_email(prompt):
    while True:
        try:
            email = input(prompt).strip()
            validate_email(email)
            return email
        except ValueError as e:
            print(f"  ✗ {e}")


def input_performance(prompt):
    while True:
        try:
            score = input_float(prompt)
            validate_performance_score(score)
            return score
        except ValueError as e:
            print(f"  ✗ {e}")


def press_enter():
    input("\n  [Nhấn Enter để tiếp tục...]")


# ─── Menu hiển thị ───────────────────────────────────────────────────────────

def show_main_menu():
    print("\n" + format_title("HỆ THỐNG QUẢN LÝ NHÂN VIÊN CÔNG TY ABC"))
    menu = [
        ("1", "Thêm nhân viên mới"),
        ("2", "Hiển thị danh sách nhân viên"),
        ("3", "Tìm kiếm nhân viên"),
        ("4", "Quản lý lương"),
        ("5", "Quản lý dự án"),
        ("6", "Đánh giá hiệu suất"),
        ("7", "Quản lý nhân sự"),
        ("8", "Thống kê báo cáo"),
        ("9", "Thoát"),
    ]
    for num, label in menu:
        print(f"  {num}. {label}")
    print(format_separator())


# ─── Chức năng 1: Thêm nhân viên ─────────────────────────────────────────────

def menu_add_employee():
    print("\n--- THÊM NHÂN VIÊN MỚI ---")
    print("  a. Thêm Manager")
    print("  b. Thêm Developer")
    print("  c. Thêm Intern")
    choice = input("  Chọn (a/b/c): ").strip().lower()
    if choice not in ('a', 'b', 'c'):
        print("  ✗ Lựa chọn không hợp lệ")
        return

    emp_id   = input("  Nhập ID      : ").strip()
    name     = input("  Họ tên       : ").strip()
    age      = input_age("  Tuổi (18-65) : ")
    email    = input_email("  Email        : ")
    dept     = input("  Phòng ban    : ").strip()
    salary   = input_salary("  Lương cơ bản : ")

    try:
        if choice == 'a':
            team = input_int("  Số thành viên nhóm: ")
            emp = Manager(emp_id, name, age, email, dept, salary, team)
        elif choice == 'b':
            lang = input("  Ngôn ngữ lập trình: ").strip() or "Python"
            emp = Developer(emp_id, name, age, email, dept, salary, lang)
        else:
            school = input("  Trường đại học: ").strip()
            emp = Intern(emp_id, name, age, email, dept, salary, school)

        added = company.add_employee(emp)
        print(f"\n  ✓ Đã thêm nhân viên: {added.name} (ID: {added.employee_id})")
    except (InvalidAgeError, InvalidSalaryError) as e:
        print(f"  ✗ {e}")
    press_enter()


# ─── Chức năng 2: Hiển thị danh sách ─────────────────────────────────────────

def menu_show_employees():
    print("\n--- HIỂN THỊ DANH SÁCH NHÂN VIÊN ---")
    print("  a. Tất cả nhân viên")
    print("  b. Theo loại (Manager/Developer/Intern)")
    print("  c. Theo hiệu suất (từ cao đến thấp)")
    choice = input("  Chọn (a/b/c): ").strip().lower()

    try:
        if choice == 'a':
            employees = company.get_all_employees()
            print(f"\n  Tổng số: {len(employees)} nhân viên\n")
        elif choice == 'b':
            role = input("  Loại (Manager/Developer/Intern): ").strip()
            employees = company.get_employees_by_role(role)
            print(f"\n  Tìm thấy {len(employees)} {role}\n")
        elif choice == 'c':
            employees = company.get_employees_by_performance()
            print(f"\n  Danh sách theo hiệu suất (cao → thấp):\n")
        else:
            print("  ✗ Lựa chọn không hợp lệ")
            return

        for emp in employees:
            print(f"  {emp}")
    except IndexError as e:
        print(f"  ⚠ {e}")
    press_enter()


# ─── Chức năng 3: Tìm kiếm ───────────────────────────────────────────────────

def menu_search():
    print("\n--- TÌM KIẾM NHÂN VIÊN ---")
    print("  a. Theo ID")
    print("  b. Theo tên")
    print("  c. Theo ngôn ngữ lập trình (Developer)")
    choice = input("  Chọn (a/b/c): ").strip().lower()

    try:
        if choice == 'a':
            eid = input("  Nhập ID: ").strip()
            emp = company.find_by_id(eid)
            print()
            print(format_employee_info(emp))
        elif choice == 'b':
            name = input("  Nhập tên: ").strip()
            results = company.find_by_name(name)
            print(f"\n  Tìm thấy {len(results)} nhân viên:")
            for emp in results:
                print(f"  {emp}")
        elif choice == 'c':
            lang = input("  Nhập ngôn ngữ: ").strip()
            results = company.find_by_language(lang)
            print(f"\n  Tìm thấy {len(results)} Developer:")
            for emp in results:
                print(f"  {emp}")
        else:
            print("  ✗ Lựa chọn không hợp lệ")
    except EmployeeNotFoundError as e:
        print(f"  ⚠ {e}")
    press_enter()


# ─── Chức năng 4: Lương ──────────────────────────────────────────────────────

def menu_salary():
    print("\n--- QUẢN LÝ LƯƠNG ---")
    print("  a. Tính lương cho từng nhân viên")
    print("  b. Tính tổng lương công ty")
    print("  c. Top 3 nhân viên lương cao nhất")
    choice = input("  Chọn (a/b/c): ").strip().lower()

    try:
        employees = company.get_all_employees()
    except IndexError as e:
        print(f"  ⚠ {e}")
        press_enter()
        return

    if choice == 'a':
        try:
            eid = input("  Nhập ID nhân viên: ").strip()
            emp = company.find_by_id(eid)
            sal = Payroll.calculate_employee_salary(emp)
            print(f"\n  Nhân viên : {emp.name}")
            print(f"  Lương CB  : {format_currency(emp.base_salary)}")
            print(f"  Lương thực: {format_currency(sal)}")
        except EmployeeNotFoundError as e:
            print(f"  ⚠ {e}")
    elif choice == 'b':
        total = Payroll.calculate_total_salary(employees)
        print(f"\n  Tổng lương công ty: {format_currency(total)}")
        dept_sal = Payroll.get_salary_by_department(employees)
        print("\n  Theo phòng ban:")
        for dept, sal in dept_sal.items():
            print(f"    {dept}: {format_currency(sal)}")
    elif choice == 'c':
        top = Payroll.get_top_salary(employees, 3)
        print("\n  Top 3 lương cao nhất:")
        for i, emp in enumerate(top, 1):
            print(f"  {i}. {emp.name} ({emp.get_role()}) - {format_currency(emp.calculate_salary())}")
    else:
        print("  ✗ Lựa chọn không hợp lệ")
    press_enter()


# ─── Chức năng 5: Dự án ──────────────────────────────────────────────────────

def menu_projects():
    print("\n--- QUẢN LÝ DỰ ÁN ---")
    print("  a. Phân công nhân viên vào dự án")
    print("  b. Xóa nhân viên khỏi dự án")
    print("  c. Hiển thị dự án của 1 nhân viên")
    choice = input("  Chọn (a/b/c): ").strip().lower()

    try:
        if choice == 'a':
            eid     = input("  ID nhân viên: ").strip()
            project = input("  Tên dự án   : ").strip()
            company.assign_project(eid, project)
            print(f"  ✓ Đã phân công vào dự án '{project}'")
        elif choice == 'b':
            eid     = input("  ID nhân viên: ").strip()
            project = input("  Tên dự án   : ").strip()
            company.remove_from_project(eid, project)
            print(f"  ✓ Đã xóa khỏi dự án '{project}'")
        elif choice == 'c':
            eid      = input("  ID nhân viên: ").strip()
            projects = company.get_employee_projects(eid)
            emp      = company.find_by_id(eid)
            if projects:
                print(f"\n  Dự án của {emp.name}: {', '.join(projects)}")
            else:
                print(f"\n  {emp.name} chưa tham gia dự án nào")
        else:
            print("  ✗ Lựa chọn không hợp lệ")
    except EmployeeNotFoundError as e:
        print(f"  ⚠ {e}")
    except ProjectAllocationError as e:
        print(f"  ✗ {e}")
    except ValueError as e:
        print(f"  ✗ {e}")
    press_enter()


# ─── Chức năng 6: Hiệu suất ──────────────────────────────────────────────────

def menu_performance():
    print("\n--- ĐÁNH GIÁ HIỆU SUẤT ---")
    print("  a. Cập nhật điểm hiệu suất cho nhân viên")
    print("  b. Hiển thị nhân viên xuất sắc (điểm > 8)")
    print("  c. Hiển thị nhân viên cần cải thiện (điểm < 5)")
    choice = input("  Chọn (a/b/c): ").strip().lower()

    try:
        if choice == 'a':
            eid   = input("  ID nhân viên   : ").strip()
            score = input_performance("  Điểm (0-10)    : ")
            company.update_performance(eid, score)
            emp = company.find_by_id(eid)
            print(f"  ✓ Đã cập nhật điểm cho {emp.name}: {score}/10")
        elif choice == 'b':
            result = company.get_excellent_employees()
            print(f"\n  Nhân viên xuất sắc ({len(result)} người):")
            for emp in result:
                print(f"  ★ {emp.name} ({emp.get_role()}) - Điểm: {emp.performance_score}")
        elif choice == 'c':
            result = company.get_needs_improvement()
            print(f"\n  Nhân viên cần cải thiện ({len(result)} người):")
            for emp in result:
                print(f"  ! {emp.name} ({emp.get_role()}) - Điểm: {emp.performance_score}")
        else:
            print("  ✗ Lựa chọn không hợp lệ")
    except EmployeeNotFoundError as e:
        print(f"  ⚠ {e}")
    except IndexError as e:
        print(f"  ⚠ {e}")
    press_enter()


# ─── Chức năng 7: Nhân sự ────────────────────────────────────────────────────

def menu_hr():
    print("\n--- QUẢN LÝ NHÂN SỰ ---")
    print("  a. Xóa nhân viên (nghỉ việc)")
    print("  b. Tăng lương cơ bản")
    print("  c. Thăng chức (Intern→Developer, Developer→Manager)")
    choice = input("  Chọn (a/b/c): ").strip().lower()

    try:
        if choice == 'a':
            eid = input("  ID nhân viên: ").strip()
            emp = company.remove_employee(eid)
            print(f"  ✓ Đã xóa nhân viên: {emp.name}")
        elif choice == 'b':
            eid    = input("  ID nhân viên    : ").strip()
            amount = input_salary("  Số tiền tăng    : ")
            company.raise_salary(eid, amount)
            emp = company.find_by_id(eid)
            print(f"  ✓ Lương mới của {emp.name}: {format_currency(emp.base_salary)}")
        elif choice == 'c':
            eid = input("  ID nhân viên: ").strip()
            old_role, new_role, emp = company.promote(eid)
            print(f"  ✓ Đã thăng chức {emp.name}: {old_role} → {new_role}")
        else:
            print("  ✗ Lựa chọn không hợp lệ")
    except EmployeeNotFoundError as e:
        print(f"  ⚠ {e}")
    except ValueError as e:
        print(f"  ✗ {e}")
    press_enter()


# ─── Chức năng 8: Báo cáo ────────────────────────────────────────────────────

def menu_report():
    print("\n--- THỐNG KÊ BÁO CÁO ---")
    print("  a. Số lượng nhân viên theo loại")
    print("  b. Tổng lương theo phòng ban")
    print("  c. Số dự án trung bình trên mỗi nhân viên")
    choice = input("  Chọn (a/b/c): ").strip().lower()

    try:
        employees = company.get_all_employees()
    except IndexError as e:
        print(f"  ⚠ {e}")
        press_enter()
        return

    if choice == 'a':
        counts = Payroll.count_by_role(employees)
        print("\n  Số lượng theo loại:")
        for role, count in counts.items():
            print(f"    {role:12s}: {count} người")
        print(f"    {'Tổng':12s}: {len(employees)} người")
    elif choice == 'b':
        dept_sal = Payroll.get_salary_by_department(employees)
        print("\n  Tổng lương theo phòng ban:")
        for dept, sal in dept_sal.items():
            print(f"    {dept:20s}: {format_currency(sal)}")
    elif choice == 'c':
        avg = Payroll.avg_projects_per_employee(employees)
        print(f"\n  Số dự án trung bình: {avg:.2f} dự án/nhân viên")
    else:
        print("  ✗ Lựa chọn không hợp lệ")
    press_enter()


# ─── Dữ liệu mẫu ─────────────────────────────────────────────────────────────

def load_sample_data():
    """Nạp dữ liệu mẫu để demo"""
    sample = [
        Manager("MGR001", "Nguyễn Văn An", 35, "an.nguyen@abc.com", "Kỹ thuật", 20_000_000, 5),
        Manager("MGR002", "Trần Thị Bình", 40, "binh.tran@abc.com", "Kinh doanh", 22_000_000, 8),
        Developer("DEV001", "Lê Văn Cường", 28, "cuong.le@abc.com", "Kỹ thuật", 15_000_000, "Python"),
        Developer("DEV002", "Phạm Thị Dung", 26, "dung.pham@abc.com", "Kỹ thuật", 14_000_000, "JavaScript"),
        Developer("DEV003", "Hoàng Văn Em", 30, "em.hoang@abc.com", "Kỹ thuật", 16_000_000, "Java"),
        Intern("INT001", "Ngô Thị Phương", 22, "phuong.ngo@abc.com", "Kỹ thuật", 5_000_000, "ĐH Bách Khoa"),
        Intern("INT002", "Vũ Văn Giang", 21, "giang.vu@abc.com", "Kinh doanh", 4_500_000, "ĐH Kinh Tế"),
    ]
    for emp in sample:
        company.add_employee(emp)

    # Gán dự án và điểm hiệu suất mẫu
    company.assign_project("MGR001", "Dự án Alpha")
    company.assign_project("DEV001", "Dự án Alpha")
    company.assign_project("DEV001", "Dự án Beta")
    company.assign_project("DEV002", "Dự án Beta")
    company.update_performance("MGR001", 9.0)
    company.update_performance("MGR002", 8.5)
    company.update_performance("DEV001", 9.2)
    company.update_performance("DEV002", 7.5)
    company.update_performance("DEV003", 4.0)
    company.update_performance("INT001", 8.8)
    company.update_performance("INT002", 3.5)


# ─── Vòng lặp chính ──────────────────────────────────────────────────────────

def main():
    print(format_title("KHỞI ĐỘNG HỆ THỐNG"))
    load = input("  Nạp dữ liệu mẫu? (y/n): ").strip().lower()
    if load == 'y':
        load_sample_data()
        print(f"  ✓ Đã nạp {len(company.employees)} nhân viên mẫu")

    while True:
        show_main_menu()
        choice = input("  Chọn chức năng (1-9): ").strip()

        if choice == '1':
            menu_add_employee()
        elif choice == '2':
            menu_show_employees()
        elif choice == '3':
            menu_search()
        elif choice == '4':
            menu_salary()
        elif choice == '5':
            menu_projects()
        elif choice == '6':
            menu_performance()
        elif choice == '7':
            menu_hr()
        elif choice == '8':
            menu_report()
        elif choice == '9':
            print("\n  Tạm biệt! Hẹn gặp lại.\n")
            break
        else:
            print("  ✗ Vui lòng chọn từ 1 đến 9")


if __name__ == "__main__":
    main()