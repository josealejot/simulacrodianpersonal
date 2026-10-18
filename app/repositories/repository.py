import json
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Module, Topic, Question, Option, Flashcard, ExamAttempt, DocumentResource

class DIANRepository:
    @staticmethod
    def get_modules(db: Session) -> List[Module]:
        return db.query(Module).order_by(Module.number.asc()).all()

    @staticmethod
    def get_module_by_id(db: Session, module_id: int) -> Optional[Module]:
        return db.query(Module).filter(Module.id == module_id).first()

    @staticmethod
    def get_module_by_number(db: Session, number: int) -> Optional[Module]:
        return db.query(Module).filter(Module.number == number).first()

    @staticmethod
    def get_questions_by_module(db: Session, module_id: int) -> List[Question]:
        return db.query(Question).filter(Question.module_id == module_id).all()

    @staticmethod
    def get_all_questions(db: Session) -> List[Question]:
        return db.query(Question).order_by(Question.id.asc()).all()

    @staticmethod
    def get_flashcards(db: Session, module_id: Optional[int] = None) -> List[Flashcard]:
        query = db.query(Flashcard)
        if module_id:
            query = query.filter(Flashcard.module_id == module_id)
        return query.order_by(Flashcard.id.asc()).all()

    @staticmethod
    def get_documents(db: Session, category: Optional[str] = None) -> List[DocumentResource]:
        query = db.query(DocumentResource)
        if category:
            query = query.filter(DocumentResource.category == category)
        return query.order_by(DocumentResource.category.asc(), DocumentResource.id.asc()).all()

    @staticmethod
    def get_question_by_id(db: Session, question_id: int) -> Optional[Question]:
        return db.query(Question).filter(Question.id == question_id).first()

    @staticmethod
    def save_exam_attempt(db: Session, attempt_data: Dict[str, Any]) -> ExamAttempt:
        attempt = ExamAttempt(
            duration_seconds=attempt_data.get("duration_seconds", 0),
            total_questions=attempt_data["total_questions"],
            correct_answers=attempt_data["correct_answers"],
            functional_score=attempt_data["functional_score"],
            behavioral_score=attempt_data["behavioral_score"],
            integrity_score=attempt_data["integrity_score"],
            total_weighted_score=attempt_data["total_weighted_score"],
            passed_functional=attempt_data["passed_functional"],
            details_json=json.dumps(attempt_data.get("details", {}), ensure_ascii=False)
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        return attempt

    @staticmethod
    def get_exam_attempts(db: Session, limit: int = 15) -> List[ExamAttempt]:
        return db.query(ExamAttempt).order_by(ExamAttempt.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_statistics(db: Session) -> Dict[str, Any]:
        attempts = db.query(ExamAttempt).all()
        total_attempts = len(attempts)
        if total_attempts == 0:
            return {
                "total_attempts": 0,
                "passed_count": 0,
                "failed_count": 0,
                "pass_rate": 0.0,
                "avg_weighted_score": 0.0,
                "avg_functional_score": 0.0,
                "highest_score": 0.0,
                "recent_history": []
            }

        passed_count = sum(1 for a in attempts if a.passed_functional)
        avg_weighted = sum(a.total_weighted_score for a in attempts) / total_attempts
        avg_functional = sum(a.functional_score for a in attempts) / total_attempts
        highest_score = max(a.total_weighted_score for a in attempts)

        history = [
            {
                "id": a.id,
                "date": a.created_at.strftime("%Y-%m-%d %H:%M"),
                "total_weighted_score": round(a.total_weighted_score, 2),
                "functional_score": round(a.functional_score, 2),
                "passed_functional": a.passed_functional,
                "correct_answers": a.correct_answers,
                "total_questions": a.total_questions
            }
            for a in sorted(attempts, key=lambda x: x.created_at, reverse=True)[:10]
        ]

        return {
            "total_attempts": total_attempts,
            "passed_count": passed_count,
            "failed_count": total_attempts - passed_count,
            "pass_rate": round((passed_count / total_attempts) * 100, 1),
            "avg_weighted_score": round(avg_weighted, 2),
            "avg_functional_score": round(avg_functional, 2),
            "highest_score": round(highest_score, 2),
            "recent_history": history
        }
