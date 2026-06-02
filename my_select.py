import os
from sqlalchemy import create_engine, select, func, desc, and_
from sqlalchemy.orm import sessionmaker

# Import models
from models import Group, Student, Teacher, Subject, Grade

# Setup database connection securely
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def select_1(session):
    """
    1. Find the 5 students with the highest average grade across all subjects.
    """
    stmt = (
        select(
            Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
    )
    return session.execute(stmt).all()


def select_2(session, subject_id: int):
    """
    2. Find the student with the highest average grade in a specific subject.
    """
    stmt = (
        select(
            Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .join(Grade)
        .group_by(Student.id)
        .filter(Grade.subject_id == subject_id)
        .order_by(desc("avg_grade"))
        .limit(1)
    )
    return session.execute(stmt).first()


def select_3(session, subject_id: int):
    """
    3. Find the average grade in groups for a specific subject.
    """
    stmt = (
        select(Group.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .order_by(desc("avg_grade"))
    )
    return session.execute(stmt).all()


def select_4(session):
    """
    4. Find the average grade across the entire flow (all grades).
    """
    stmt = select(func.round(func.avg(Grade.grade)).label("avr_grade_all"))
    return session.execute(stmt).scalar()


def select_5(session, teacher_id: int):
    """
    5. Find the subjects taught by a specific teacher.
    """
    stmt = select(Subject.name).where(Subject.teacher_id == teacher_id)
    return session.execute(stmt).scalars().all()


def select_6(session, group_id: int):
    """
    6. Find a list of students in a specific group.
    """
    stmt = select(Student.fullname).where(Student.group_id == group_id)
    return session.execute(stmt).scalars().all()


def select_7(session, group_id: int, subject_id: int):
    """
    7. Find the grades of students in a specific group for a specific subject.
    """
    stmt = (
        select(Student.fullname, Grade.grade)
        .join(Grade)
        .filter(and_(Student.group_id == group_id, Grade.subject_id == subject_id))
    )
    return session.execute(stmt).all()


def select_8(session, teacher_id: int):
    """
    8. Find the average grade a teacher gives to their students.
    """
    stmt = (
        select(func.round(func.avg(Grade.grade), 2).label('teacher_avg'))
        .select_from(Grade)
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
    )
    return session.execute(stmt).scalar()


def select_9(session, student_id: int):
    """9. Find the list of courses attended by a specific student."""
    stmt = (
        select(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .group_by(Subject.id) 
    )
    return session.execute(stmt).scalars().all()

def select_10(session, student_id: int, teacher_id: int):
    """10. Find the list of courses taught to a specific student by a specific teacher."""
    stmt = (
        select(Subject.name)
        .join(Grade)
        .filter(and_(Grade.student_id == student_id, Subject.teacher_id == teacher_id))
        .group_by(Subject.id)
    )
    return session.execute(stmt).scalars().all()


if __name__ == "__main__":
    with SessionLocal() as session:
        print("Query 1: Top 5 students overall")
        print(select_1(session))
        
        print("\nQuery 2: Top student in Subject ID 1")
        print(select_2(session, subject_id=1))
        
        print("\nQuery 3: Average grade in groups for Subject ID 3")
        print(select_3(session, subject_id=3))
        
        print("\nQuery 4: Overall average grade")
        print(select_4(session))
        
        print("\nQuery 5: Subjects taught by Teacher ID 2")
        print(select_5(session, teacher_id=1))
        
        print("\nQuery 6: Students in Group ID 3")
        print(select_6(session, group_id=1))
        
        print("\nQuery 7: Grades in Group ID 2 for Subject ID 5")
        print(select_7(session, group_id=1, subject_id=1))
        
        print("\nQuery 8: Average grade given by Teacher ID 4")
        print(select_8(session, teacher_id=1))
        
        print("\nQuery 9: Subjects attended by Student ID 7")
        print(select_9(session, student_id=1))
        
        print("\nQuery 10: Subjects taught to Student ID 1 by Teacher ID 2")
        print(select_10(session, student_id=1, teacher_id=1))
