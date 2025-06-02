# IMPORTS
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

# DATABASE SETUP

engine = create_engine("sqlite:///store.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# MODELS

class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    class_id = Column(Integer)
    gender = Column(String)

class Teachers(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    subject_id = Column(Integer)

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    date = Column(String)
    status = Column(String, nullable=False)

class Grades(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    subject_id = Column(Integer)
    grade = Column(Integer)
    term = Column(Integer)

class Classroom(Base):
    __tablename__ = "classroom"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer)

class Enrollment(Base):
    __tablename__ = "enrollment"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    subject_id = Column(Integer)
    enrollment_date = Column(Integer)

# CREATE TABLES

Base.metadata.create_all(engine)

# UTILITY FUNCTIONS

def get_student_by_email(email):
    return session.query(Students).filter_by(email=email).first()

def get_teacher_by_email(email):
    return session.query(Teachers).filter_by(email=email).first()

# CRUD OPERATIONS

def add_student():
    name = input("Enter student name: ")
    email = input("Enter email: ")
    class_id = input("Enter class ID: ")
    gender = input("Enter gender: ")
    if get_student_by_email(email):
        print(f"Student already exists: {email}")
        return
    try:
        student = Students(name=name, email=email, class_id=class_id, gender=gender)
        session.add(student)
        session.commit()
        print(f"{name} added successfully.")
    except IntegrityError:
        session.rollback()
        print("Error: Email already exists.")

def list_students():
    students = session.query(Students).all()
    if not students:
        print("No students found.")
    for s in students:
        print(f"[{s.id}] {s.name} | {s.email} | Class ID: {s.class_id} | Gender: {s.gender}")

def add_teacher():
    name = input("Enter teacher name: ")
    email = input("Enter email: ")
    subject_id = input("Enter subject ID: ")
    if get_teacher_by_email(email):
        print(f"Teacher already exists: {email}")
        return
    try:
        teacher = Teachers(name=name, email=email, subject_id=subject_id)
        session.add(teacher)
        session.commit()
        print(f"{name} added successfully.")
    except IntegrityError:
        session.rollback()
        print("Error: Email already exists.")

def list_teachers():
    teachers = session.query(Teachers).all()
    if not teachers:
        print("No teachers found.")
    for t in teachers:
        print(f"[{t.id}] {t.name} | {t.email} | Subject ID: {t.subject_id}")

def mark_attendance():
    student_id = input("Enter student ID: ")
    date = input("Enter date (YYYY-MM-DD): ")
    status = input("Enter status (Present/Absent): ")
    attendance = Attendance(student_id=student_id, date=date, status=status)
    session.add(attendance)
    session.commit()
    print(f"Attendance marked for student ID {student_id} on {date} as {status}.")

def view_grades():
    student_email = input("Enter student email to view grades: ")
    student = get_student_by_email(student_email)
    if not student:
        print("No such student.")
        return
    grades = session.query(Grades).filter_by(student_id=student.id).all()
    if not grades:
        print("No grades found for this student.")
    else:
        print(f"Grades for {student.name}:")
        for g in grades:
            print(f"Subject ID: {g.subject_id} | Grade: {g.grade} | Term: {g.term}")

# MAIN MENU
def main():
    actions = {
        "1": add_student,
        "2": list_students,
        "3": add_teacher,
        "4": list_teachers,
        "5": mark_attendance,
        "6": view_grades,
    }

    while True:
        print("\n--- School Management System ---")
        print("0. Exit")
        print("1. Add Student")
        print("2. List Students")
        print("3. Add Teacher")
        print("4. List Teachers")
        print("5. Mark Attendance")
        print("6. View Student Grades")
        choice = input("Enter an option: ")

        if choice == "0":
            print("Goodbye!")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()











    


