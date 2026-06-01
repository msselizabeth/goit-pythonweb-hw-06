import os
import random
from datetime import date
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Group, Student, Teacher, Subject, Grade

# Initialize Faker
fake = Faker()

# Setup database connection securely
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def seed_database():
    with Session() as session:
        try:
            # Groups
            for _ in range(3):
                group_name = fake.bothify(text="Group-###")
                group = Group(name=group_name)
                session.add(group)

            # Teachers
            for _ in range(5):
                teacher = Teacher(fullname=fake.name())
                session.add(teacher)

            session.commit()

            # Fetch the created groups and teachers to get their IDs
            db_groups = session.query(Group).all()
            db_teachers = session.query(Teacher).all()

            # Subjects
            SUBJECTS_LIST = [
                "Mathematics",
                "Biology",
                "Chemistry",
                "Physics",
                "Geography",
                "History",
                "English",
                "Computer Science",
            ]

            for subject_name in SUBJECTS_LIST:
                teacher = random.choice(db_teachers)
                subject = Subject(name=subject_name, teacher_id=teacher.id)
                session.add(subject)

            session.commit()
            db_subjects = session.query(Subject).all()

            # Students
            for i in range(50):
                group = random.choice(db_groups)
                student = Student(fullname=fake.name(), group_id=group.id)
                session.add(student)

            session.commit()
            db_students = session.query(Student).all()

            # Grades
            for student in db_students:
                # Random number of grades between 5 and 20 for each student
                for _ in range(random.randint(5, 20)):
                    random_subject = random.choice(db_subjects)
                    
                    grade = Grade(
                        grade=fake.random_int(min=40, max=100),
                        grade_date=fake.date_between(start_date='-1y', end_date='today'),
                        student_id=student.id,
                        subject_id=random_subject.id,
                    )
                    session.add(grade)

            # Final commit to save all grades
            session.commit()
            print("Database seeded successfully!")

        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    seed_database()
