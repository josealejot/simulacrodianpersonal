from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class OptionBase(BaseModel):
    id: int
    letter: str
    text: str
    is_correct: Optional[bool] = None

    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    id: int
    module_id: int
    category: str
    case_study: str
    question_text: str
    explanation: Optional[str] = None
    legal_reference: Optional[str] = None
    options: List[OptionBase] = []

    class Config:
        from_attributes = True

class TopicBase(BaseModel):
    id: int
    module_id: int
    title: str
    order: int
    legal_basis: Optional[str] = None
    content: str

    class Config:
        from_attributes = True

class FlashcardBase(BaseModel):
    id: int
    module_id: int
    term: str
    definition: str
    legal_norm: Optional[str] = None
    category: str

    class Config:
        from_attributes = True

class DocumentResourceBase(BaseModel):
    id: int
    title: str
    category: str
    description: str
    external_url: str
    file_type: str

    class Config:
        from_attributes = True

class ModuleSummary(BaseModel):
    id: int
    number: int
    title: str
    subtitle: Optional[str] = None
    category: str
    priority: str
    icon: str
    description: Optional[str] = None
    topics_count: int = 0
    questions_count: int = 0
    flashcards_count: int = 0

    class Config:
        from_attributes = True

class ModuleDetail(ModuleSummary):
    topics: List[TopicBase] = []

    class Config:
        from_attributes = True

class ExamAnswerItem(BaseModel):
    question_id: int
    selected_option_id: Optional[int] = None

class ExamSubmission(BaseModel):
    duration_seconds: int
    answers: List[ExamAnswerItem]

class ExamResultReviewItem(BaseModel):
    question_id: int
    category: str
    case_study: str
    question_text: str
    selected_option_id: Optional[int]
    correct_option_id: int
    is_correct: bool
    explanation: str
    legal_reference: Optional[str]
    options: List[OptionBase]

class ExamResult(BaseModel):
    attempt_id: int
    created_at: datetime
    duration_seconds: int
    total_questions: int
    correct_answers: int
    functional_score: float
    behavioral_score: float
    integrity_score: float
    total_weighted_score: float
    passed_functional: bool
    status_message: str
    module_breakdown: Dict[str, Dict[str, Any]]
    questions_review: List[ExamResultReviewItem]

class ConvocatoriaInfo(BaseModel):
    proceso: str
    cargo: str
    nivel: str
    grado: int
    codigo: int
    opec: int
    ficha: str
    subproceso: str
    vacantes: int
    ciudades: List[str]
    pesos: Dict[str, float]
    min_funcional: float
