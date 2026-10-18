/**
 * PrepDIAN 2676 - API Client Layer
 */
const API = {
  async getConvocatoria() {
    const res = await fetch('/api/convocatoria');
    if (!res.ok) throw new Error('Error al cargar datos de convocatoria');
    return await res.json();
  },

  async getModules() {
    const res = await fetch('/api/modules');
    if (!res.ok) throw new Error('Error al obtener lista de módulos');
    return await res.json();
  },

  async getModuleDetail(id) {
    const res = await fetch(`/api/modules/${id}`);
    if (!res.ok) throw new Error('Error al cargar módulo de estudio');
    return await res.json();
  },

  async getModuleQuestions(id) {
    const res = await fetch(`/api/modules/${id}/questions`);
    if (!res.ok) throw new Error('Error al cargar preguntas de práctica');
    return await res.json();
  },

  async getExamQuestions() {
    const res = await fetch('/api/exam/questions');
    if (!res.ok) throw new Error('Error al obtener preguntas de simulacro');
    return await res.json();
  },

  async submitExam(answers, durationSeconds) {
    const payload = {
      duration_seconds: durationSeconds,
      answers: answers
    };
    const res = await fetch('/api/exam/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Error al calificar simulacro');
    return await res.json();
  },

  async getExamStatistics() {
    const res = await fetch('/api/exam/statistics');
    if (!res.ok) throw new Error('Error al cargar estadísticas');
    return await res.json();
  },

  async getFlashcards(moduleId = null) {
    const url = moduleId ? `/api/flashcards?module_id=${moduleId}` : '/api/flashcards';
    const res = await fetch(url);
    if (!res.ok) throw new Error('Error al cargar flashcards');
    return await res.json();
  },

  async getDocuments(category = null) {
    const url = category && category !== 'all' ? `/api/v1/documents?category=${encodeURIComponent(category)}` : '/api/v1/documents';
    const res = await fetch(url);
    if (!res.ok) throw new Error('Error al cargar biblioteca normativa');
    return await res.json();
  }
};
