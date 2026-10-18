from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.models import Question, Option
from app.schemas.schemas import ExamSubmission, ExamResult, ExamResultReviewItem

class ScoringService:
    @staticmethod
    def evaluate_exam(db: Session, submission: ExamSubmission) -> Tuple[Dict[str, Any], List[ExamResultReviewItem]]:
        answers_map = {a.question_id: a.selected_option_id for a in submission.answers}
        
        # Load questions submitted
        question_ids = list(answers_map.keys())
        questions = db.query(Question).filter(Question.id.in_(question_ids)).all()
        
        # Categorized counts
        category_stats = {
            "Funcional": {"total": 0, "correct": 0, "weight": settings.WEIGHT_FUNCTIONAL},
            "Comportamental": {"total": 0, "correct": 0, "weight": settings.WEIGHT_BEHAVIORAL},
            "Integridad": {"total": 0, "correct": 0, "weight": settings.WEIGHT_INTEGRITY}
        }
        
        module_breakdown: Dict[str, Dict[str, Any]] = {}
        reviews: List[ExamResultReviewItem] = []
        
        total_questions = len(questions)
        total_correct = 0

        for q in questions:
            cat = q.category if q.category in category_stats else "Funcional"
            category_stats[cat]["total"] += 1
            
            # Module grouping
            mod_title = q.module.title if q.module else f"Módulo {q.module_id}"
            if mod_title not in module_breakdown:
                module_breakdown[mod_title] = {"total": 0, "correct": 0, "category": cat}
            module_breakdown[mod_title]["total"] += 1

            selected_opt_id = answers_map.get(q.id)
            correct_opt = next((opt for opt in q.options if opt.is_correct), None)
            correct_opt_id = correct_opt.id if correct_opt else -1
            
            is_correct = (selected_opt_id == correct_opt_id)
            if is_correct:
                category_stats[cat]["correct"] += 1
                module_breakdown[mod_title]["correct"] += 1
                total_correct += 1

            reviews.append(ExamResultReviewItem(
                question_id=q.id,
                category=cat,
                case_study=q.case_study,
                question_text=q.question_text,
                selected_option_id=selected_opt_id,
                correct_option_id=correct_opt_id,
                is_correct=is_correct,
                explanation=q.explanation,
                legal_reference=q.legal_reference,
                options=[
                    {
                        "id": opt.id,
                        "letter": opt.letter,
                        "text": opt.text,
                        "is_correct": opt.is_correct
                    }
                    for opt in sorted(q.options, key=lambda x: x.letter)
                ]
            ))

        # Calculate scores out of 100 per category
        def calc_cat_score(cat_name: str) -> float:
            data = category_stats[cat_name]
            if data["total"] == 0:
                return 100.0  # default neutral if no questions
            return round((data["correct"] / data["total"]) * 100.0, 2)

        func_score = calc_cat_score("Funcional")
        comp_score = calc_cat_score("Comportamental")
        integ_score = calc_cat_score("Integridad")

        # Official CNSC Rule: Functional is eliminatory (minimum 70.0/100)
        passed_functional = func_score >= settings.MIN_FUNCTIONAL_SCORE

        # Weighted score (Functional 65% + Comportamental 15% + Integridad 10% = 90% exam weight)
        # Scaled to 100-point equivalent for test performance:
        # Total official points earned on written phase (out of 90 maximum points)
        written_points_earned = round(
            (func_score * settings.WEIGHT_FUNCTIONAL) +
            (comp_score * settings.WEIGHT_BEHAVIORAL) +
            (integ_score * settings.WEIGHT_INTEGRITY),
            2
        )
        
        # Normalized score out of 100 for the written component (90 max):
        normalized_score = round((written_points_earned / 0.90), 2) if total_questions > 0 else 0.0

        if passed_functional:
            status_message = "¡FELICITACIONES! Has superado el umbral eliminatorio de la Prueba Funcional (≥ 70.00/100). Continúas en concurso para valoración de antecedentes."
        else:
            status_message = f"NO CLASIFICASTE. Obtuviste {func_score:.2f}/100 en la Prueba Funcional. El puntaje mínimo eliminatorio exigido por la CNSC/DIAN es de 70.00/100."

        # Add percentage to module breakdown
        for m_name, m_data in module_breakdown.items():
            tot = m_data["total"]
            corr = m_data["correct"]
            m_data["percentage"] = round((corr / tot) * 100.0, 1) if tot > 0 else 0.0

        attempt_data = {
            "duration_seconds": submission.duration_seconds,
            "total_questions": total_questions,
            "correct_answers": total_correct,
            "functional_score": func_score,
            "behavioral_score": comp_score,
            "integrity_score": integ_score,
            "total_weighted_score": written_points_earned,
            "passed_functional": passed_functional,
            "status_message": status_message,
            "module_breakdown": module_breakdown,
            "details": {
                "category_stats": category_stats,
                "normalized_score": normalized_score
            }
        }

        return attempt_data, reviews
