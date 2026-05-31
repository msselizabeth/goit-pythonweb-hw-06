from datetime import date
from sqlalchemy import ForeignKey, String, Integer, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Group(Base):
    __tablename__ = "groups"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    students: Mapped[list["Student"]] = relationship(back_populates='group')


class Student(Base):
    __tablename__ = "students"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(120), nullable=False)
    group_id: Mapped[int | None] = mapped_column(ForeignKey('groups.id', ondelete="SET NULL"))
    
    group: Mapped['Group' | None] = relationship(back_populates='students')
    grades: Mapped[list["Grade"]] = relationship(back_populates='student', cascade="all, delete-orphan")


class Teacher(Base):
    __tablename__ = "teachers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(120), nullable=False)
    
    subjects: Mapped[list["Subject"]] = relationship(back_populates='teacher')


class Subject(Base):
    __tablename__ = "subjects"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    teacher_id: Mapped[int | None] = mapped_column(ForeignKey('teachers.id', ondelete="SET NULL"))
    teacher: Mapped["Teacher" | None] = relationship(back_populates='subjects')
    
    grades: Mapped[list["Grade"]] = relationship(back_populates='subject', cascade="all, delete-orphan")


class Grade(Base):
    __tablename__ = "grades"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    
    grade_date: Mapped[date] = mapped_column(Date, nullable=False)

    student_id: Mapped[int] = mapped_column(ForeignKey('students.id', ondelete="CASCADE"))
    student: Mapped["Student"] = relationship(back_populates='grades')
       
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id', ondelete="CASCADE"))
    subject: Mapped["Subject"] = relationship(back_populates='grades')