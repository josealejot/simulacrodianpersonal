/**
 * PrepDIAN 2676 - Centralized Reactive State
 */
const AppState = {
  activeView: 'dashboard',
  convocatoria: null,
  modules: [],
  selectedModule: null,
  moduleQuestions: [],
  
  // Estado del Simulacro
  exam: {
    inProgress: false,
    questions: [],
    currentIndex: 0,
    answers: {},       // { question_id: selected_option_id }
    flagged: new Set(),// Set of flagged question ids
    remainingSeconds: 60 * 30, // 30 minutos iniciales
    timerInterval: null,
    totalSecondsElapsed: 0,
    lastResult: null
  },

  // Configuración del simulacro (elegida en la pantalla previa)
  examConfig: {
    count: 40,            // número de preguntas (0 = todas)
    secondsPerQuestion: 120,
    moduleIds: [],        // vacío = todos los módulos
    label: 'Simulacro general'
  },

  // Ejes temáticos OPEC (cache de /api/ejes)
  ejes: null,

  // Estado de Flashcards
  flashcards: {
    items: [],
    currentIndex: 0,
    isFlipped: false,
    selectedModuleId: 'all'
  },

  // Estado de Biblioteca Normativa
  documents: {
    items: [],
    selectedCategory: 'all'
  },

  // Suscriptores para reactividad
  listeners: [],

  subscribe(listener) {
    this.listeners.push(listener);
  },

  notify() {
    this.listeners.forEach(fn => fn(this));
  },

  setView(viewName) {
    this.activeView = viewName;
    this.notify();
  },

  resetExam() {
    if (this.exam.timerInterval) {
      clearInterval(this.exam.timerInterval);
    }
    this.exam.inProgress = false;
    this.exam.questions = [];
    this.exam.currentIndex = 0;
    this.exam.answers = {};
    this.exam.flagged.clear();
    this.exam.remainingSeconds = 60 * 30;
    this.exam.totalSecondsElapsed = 0;
    this.notify();
  }
};
