from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, LargeBinary, Date, Time
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    password = Column(String, nullable=True)
    cluster = Column(Integer, nullable=False)
    profile_pic = Column(LargeBinary, nullable=True)
    role = Column(String, nullable=False)  
    students = relationship('Student', back_populates='parent')

class School(Base):
    __tablename__ = 'schools'
    id = Column(Integer, primary_key=True, autoincrement=True)
    schoolid = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    cluster = Column(Integer, nullable=False)
    profile_pic = Column(LargeBinary, nullable=True)
    teachers = relationship('Teacher', back_populates='school')
    students = relationship('Student', back_populates='school')

class Playground(Base):
    __tablename__ = 'playgrounds'
    id = Column(Integer, primary_key=True, autoincrement=True)
    groundid = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    cluster = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    profile_pic = Column(LargeBinary, nullable=True)

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    school_id = Column(String, ForeignKey('schools.schoolid'), nullable=False)
    address = Column(String, nullable=False)
    password = Column(String, nullable=True)
    cluster = Column(Integer, nullable=False)
    profile_pic = Column(LargeBinary, nullable=True)
    role = Column(String, nullable=False)  
    school = relationship('School', back_populates='teachers')

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    school_id = Column(String, ForeignKey('schools.schoolid'), nullable=False)
    class_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    cluster = Column(Integer, nullable=False)
    password = Column(String, nullable=True)
    fathers_name = Column(String, nullable=False)
    profile_pic = Column(LargeBinary, nullable=True)
    role = Column(String, nullable=False)  
    parent_id = Column(String, ForeignKey('parents.email'), nullable=False)
    parent = relationship('Parent', back_populates='students')
    school = relationship('School', back_populates='students')
    tasks = relationship('Task', back_populates='student')

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String, nullable=False)
    task_date = Column(Date, nullable=False)
    task_time = Column(Time, nullable=False)
    task_deadline = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    student_id = Column(String, ForeignKey('students.email'), nullable=False)
    student = relationship('Student', back_populates='tasks')
