import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, index=True)
    title = Column(String(200), nullable=False)
    subtitle = Column(String(300), nullable=True)
    category = Column(String(100), default="Funcional")  # Funcional, Comportamental, Integridad
    priority = Column(String(50), default="Media")       # Máxima, Alta, Media
    icon = Column(String(100), default="book")
    description = Column(Text, nullable=True)

    topics = relationship("Topic", back_populates="module", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="module", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="module", cascade="all, delete-orphan")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    title = Column(String(250), nullable=False)
    order = Column(Integer, default=1)
    legal_basis = Column(String(300), nullable=True)
    content = Column(Text, nullable=False)  # Comprehensive theoretical notes

    module = relationship("Module", back_populates="topics")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    category = Column(String(100), default="Funcional") # Funcional, Comportamental, Integridad
    case_study = Column(Text, nullable=False)           # Situational judgment 3-5 lines
    question_text = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)          # Why the key is right and others are distractors
    legal_reference = Column(String(300), nullable=True)

    module = relationship("Module", back_populates="questions")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")

class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    letter = Column(String(1), nullable=False) # 'A', 'B', or 'C'
    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    question = relationship("Question", back_populates="options")

class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    term = Column(String(250), nullable=False)
    definition = Column(Text, nullable=False)
    legal_norm = Column(String(250), nullable=True)
    category = Column(String(100), default="Términos Legales")

    module = relationship("Module", back_populates="flashcards")

class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    duration_seconds = Column(Integer, default=0)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    functional_score = Column(Float, nullable=False)
    behavioral_score = Column(Float, nullable=False)
    integrity_score = Column(Float, nullable=False)
    total_weighted_score = Column(Float, nullable=False)
    passed_functional = Column(Boolean, nullable=False)
    details_json = Column(Text, nullable=True) # Full answers, question states and breakdown

class DocumentResource(Base):
    __tablename__ = "document_resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    external_url = Column(String(500), nullable=False)
    file_type = Column(String(50), default="Portal Web oficial")
