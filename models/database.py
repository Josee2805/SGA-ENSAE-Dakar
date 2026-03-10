"""models/database.py — SGA ENSAE Dakar"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH      = os.path.join(BASE_DIR, "data", "sga_ensae_dakar.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine       = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base         = declarative_base()

class Student(Base):
    __tablename__ = "students"
    id             = Column(Integer, primary_key=True, index=True)
    nom            = Column(String(100), nullable=False)
    prenom         = Column(String(100), nullable=False)
    email          = Column(String(200), unique=True, nullable=False)
    date_naissance = Column(Date, nullable=True)
    filiere        = Column(String(100), default="Statistique")
    annee          = Column(Integer, default=3)
    attendances    = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    grades         = relationship("Grade",      back_populates="student", cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = "courses"
    code         = Column(String(20),  primary_key=True)
    libelle      = Column(String(200), nullable=False)
    volume_total = Column(Integer, default=0)
    enseignant   = Column(String(200), nullable=True)
    description  = Column(Text, nullable=True)
    sessions     = relationship("Session", back_populates="course", cascade="all, delete-orphan")
    grades       = relationship("Grade",   back_populates="course", cascade="all, delete-orphan")

class Session(Base):
    __tablename__ = "sessions"
    id          = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(20), ForeignKey("courses.code"), nullable=False)
    date        = Column(Date, nullable=False)
    duree       = Column(Float, default=1.5)
    theme       = Column(Text, nullable=True)
    salle       = Column(String(50), nullable=True)
    course      = relationship("Course",     back_populates="sessions")
    attendances = relationship("Attendance", back_populates="session", cascade="all, delete-orphan")

class Attendance(Base):
    __tablename__ = "attendance"
    id_session = Column(Integer, ForeignKey("sessions.id"),  primary_key=True)
    id_student = Column(Integer, ForeignKey("students.id"),  primary_key=True)
    session    = relationship("Session", back_populates="attendances")
    student    = relationship("Student", back_populates="attendances")

class Grade(Base):
    __tablename__ = "grades"
    id          = Column(Integer, primary_key=True, index=True)
    id_student  = Column(Integer, ForeignKey("students.id"),  nullable=False)
    course_code = Column(String(20), ForeignKey("courses.code"), nullable=False)
    note        = Column(Float, nullable=False)
    coefficient = Column(Float, default=1.0)
    type_eval   = Column(String(50), default="Examen")
    student     = relationship("Student", back_populates="grades")
    course      = relationship("Course",  back_populates="grades")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    Base.metadata.create_all(bind=engine)
    print(f"[DB] Base initialisée : {DB_PATH}")

def get_db():
    return SessionLocal()
