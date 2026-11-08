import random
from collections import defaultdict
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.repositories.repository import DIANRepository
from app.services.scoring_service import ScoringService
from app.services.seed_service import SeedService
from app.services.content_opec import EJES_OPEC
from app.schemas.schemas import (
    ModuleSummary, ModuleDetail, QuestionBase, FlashcardBase,
    ExamSubmission, ExamResult, ConvocatoriaInfo, DocumentResourceBase
)

router = APIRouter()

@router.get("/v1/documents", response_model=List[DocumentResourceBase])
@router.get("/documents", response_model=List[DocumentResourceBase])
def get_documents(category: Optional[str] = None, db: Session = Depends(get_db)):
    """Devuelve la lista completa de recursos normativos ordenados por categoría"""
    return DIANRepository.get_documents(db, category)

@router.get("/convocatoria", response_model=ConvocatoriaInfo)
def get_convocatoria_info():
    return {
        "proceso": settings.PROCESO,
        "cargo": settings.CARGO,
        "nivel": settings.NIVEL,
        "grado": settings.GRADO,
        "codigo": settings.CODIGO,
        "opec": settings.OPEC,
        "ficha": settings.MANUAL_FUNCIONES_FICHA,
        "subproceso": settings.PROCESO_SUBPROCESO,
        "vacantes": settings.VACANTES,
        "ciudades": settings.CIUDADES_VACANTES,
        "pesos": {
            "funcional": settings.WEIGHT_FUNCTIONAL,
            "comportamental": settings.WEIGHT_BEHAVIORAL,
            "integridad": settings.WEIGHT_INTEGRITY,
            "antecedentes": settings.WEIGHT_BACKGROUND
        },
        "min_funcional": settings.MIN_FUNCTIONAL_SCORE
    }

@router.get("/modules", response_model=List[ModuleSummary])
def list_modules(db: Session = Depends(get_db)):
    modules = DIANRepository.get_modules(db)
    result = []
    for m in modules:
        result.append(ModuleSummary(
            id=m.id,
            number=m.number,
            title=m.title,
            subtitle=m.subtitle,
            category=m.category,
            priority=m.priority,
            icon=m.icon,
            description=m.description,
            topics_count=len(m.topics),
            questions_count=len(m.questions),
            flashcards_count=len(m.flashcards)
        ))
    return result

@router.get("/modules/{module_id}", response_model=ModuleDetail)
def get_module_detail(module_id: int, db: Session = Depends(get_db)):
    module = DIANRepository.get_module_by_id(db, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    
    return ModuleDetail(
        id=module.id,
        number=module.number,
        title=module.title,
        subtitle=module.subtitle,
        category=module.category,
        priority=module.priority,
        icon=module.icon,
        description=module.description,
        topics_count=len(module.topics),
        questions_count=len(module.questions),
        flashcards_count=len(module.flashcards),
        topics=sorted(module.topics, key=lambda t: t.order)
    )

@router.get("/modules/{module_id}/questions", response_model=List[QuestionBase])
def get_module_practice_questions(module_id: int, db: Session = Depends(get_db)):
    questions = DIANRepository.get_questions_by_module(db, module_id)
    return questions

@router.get("/ejes")
def get_ejes_opec(db: Session = Depends(get_db)):
    """Ejes temáticos oficiales de la ficha CC-AU-2010 con sus módulos de estudio."""
    modules = {m.number: m for m in DIANRepository.get_modules(db)}
    result = []
    for eje in EJES_OPEC:
        linked = [modules[n] for n in eje["modulos"] if n in modules]
        result.append({
            "numero": eje["numero"],
            "grupo": eje["grupo"],
            "titulo": eje["titulo"],
            "claves": eje["claves"],
            "modulos": [{"id": m.id, "number": m.number, "title": m.title} for m in linked],
            "questions_count": sum(len(m.questions) for m in linked),
            "flashcards_count": sum(len(m.flashcards) for m in linked),
        })
    return {
        "fecha_prueba": settings.FECHA_PRUEBA_ISO,
        "corte_normativo": settings.CORTE_NORMATIVO,
        "ejes": result,
    }

def _balanced_sample(questions, limit: int):
    """Toma preguntas en rondas por módulo para cubrir todos los ejes de forma pareja."""
    pools: Dict[int, list] = defaultdict(list)
    for q in questions:
        pools[q.module_id].append(q)
    for pool in pools.values():
        random.shuffle(pool)
    module_order = list(pools.keys())
    random.shuffle(module_order)
    picked = []
    while len(picked) < limit and any(pools.values()):
        for mid in module_order:
            if pools[mid] and len(picked) < limit:
                picked.append(pools[mid].pop())
    random.shuffle(picked)
    return picked

@router.get("/exam/questions", response_model=List[QuestionBase])
def get_exam_questions(
    limit: Optional[int] = Query(None, ge=1, le=500),
    module_ids: Optional[str] = Query(None, description="IDs de módulo separados por coma"),
    shuffle: bool = False,
    db: Session = Depends(get_db),
):
    """Devuelve las preguntas del simulacro sin revelar cuál es la respuesta correcta.
    Sin parámetros conserva el comportamiento original (todas, en orden)."""
    questions = DIANRepository.get_all_questions(db)
    if module_ids:
        try:
            wanted = {int(x) for x in module_ids.split(",") if x.strip()}
        except ValueError:
            raise HTTPException(status_code=422, detail="module_ids debe ser una lista de enteros separados por coma")
        questions = [q for q in questions if q.module_id in wanted]
    if limit is not None and limit < len(questions):
        questions = _balanced_sample(questions, limit)
    elif shuffle:
        questions = list(questions)
        random.shuffle(questions)
    result = []
    for q in questions:
        result.append(QuestionBase(
            id=q.id,
            module_id=q.module_id,
            category=q.category,
            case_study=q.case_study,
            question_text=q.question_text,
            legal_reference=q.legal_reference,
            options=[
                {
                    "id": opt.id,
                    "letter": opt.letter,
                    "text": opt.text,
                    "is_correct": None  # Oculto durante el examen
                }
                for opt in sorted(q.options, key=lambda x: x.letter)
            ]
        ))
    return result

@router.post("/exam/submit", response_model=ExamResult)
def submit_exam(submission: ExamSubmission, db: Session = Depends(get_db)):
    attempt_data, reviews = ScoringService.evaluate_exam(db, submission)
    attempt_data["details"]["reviews"] = [r.model_dump() for r in reviews]
    
    saved_attempt = DIANRepository.save_exam_attempt(db, attempt_data)
    
    return ExamResult(
        attempt_id=saved_attempt.id,
        created_at=saved_attempt.created_at,
        duration_seconds=saved_attempt.duration_seconds,
        total_questions=saved_attempt.total_questions,
        correct_answers=saved_attempt.correct_answers,
        functional_score=saved_attempt.functional_score,
        behavioral_score=saved_attempt.behavioral_score,
        integrity_score=saved_attempt.integrity_score,
        total_weighted_score=saved_attempt.total_weighted_score,
        passed_functional=saved_attempt.passed_functional,
        status_message=attempt_data["status_message"],
        module_breakdown=attempt_data["module_breakdown"],
        questions_review=reviews
    )

@router.get("/exam/statistics")
def get_exam_statistics(db: Session = Depends(get_db)):
    return DIANRepository.get_statistics(db)

@router.get("/flashcards", response_model=List[FlashcardBase])
def get_flashcards(module_id: Optional[int] = None, db: Session = Depends(get_db)):
    return DIANRepository.get_flashcards(db, module_id)

@router.post("/admin/reseed")
def reseed_database(db: Session = Depends(get_db)):
    SeedService.seed_database(db, force_reset=True)
    return {"status": "ok", "message": "Base de datos reinicializada con datos oficiales."}
