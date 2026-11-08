/**
 * PrepDIAN 2676 - UI Renderer & Interaction Controller
 */
const UI = {
  async init() {
    // Escuchar cambios de estado
    AppState.subscribe(() => this.render());

    // Cargar datos iniciales
    try {
      AppState.convocatoria = await API.getConvocatoria();
      AppState.modules = await API.getModules();
    } catch (err) {
      console.error('Error cargando datos:', err);
    }

    // Event listeners de navegación
    document.querySelectorAll('[data-nav]').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        const view = el.getAttribute('data-nav');
        this.navigateTo(view);
      });
    });

    // Atajos de teclado (simulacro y flashcards)
    document.addEventListener('keydown', (e) => this.handleKeydown(e));

    this.render();
  },

  handleKeydown(e) {
    const tag = (e.target && e.target.tagName) || '';
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(tag)) return;
    const view = AppState.activeView;

    if (view === 'exam' && AppState.exam.inProgress) {
      const q = AppState.exam.questions[AppState.exam.currentIndex];
      const key = e.key.toUpperCase();
      if (['A', 'B', 'C'].includes(key) && q) {
        const opt = q.options.find(o => o.letter === key);
        if (opt) { e.preventDefault(); this.selectExamOption(q.id, opt.id); }
      } else if (e.key === 'ArrowRight') {
        e.preventDefault(); this.nextExamQuestion();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault(); this.prevExamQuestion();
      } else if (key === 'M' && q) {
        e.preventDefault(); this.toggleFlagQuestion(q.id);
      }
    } else if (view === 'flashcards') {
      if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); this.toggleFlipFlashcard(); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); this.nextFlashcard(); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); this.prevFlashcard(); }
    }
  },

  // -------------------------------------------------------------
  // Utilidades: escape HTML y Markdown ligero para el temario
  // -------------------------------------------------------------
  esc(s) {
    return String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  },

  mdInline(s) {
    return this.esc(s)
      .replace(/`([^`]+)`/g, '<code class="px-1.5 py-0.5 rounded bg-slate-100 text-slate-800 font-mono text-[0.85em]">$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong class="hl font-semibold text-slate-900">$1</strong>')
      .replace(/(^|[^*])\*([^*\s][^*]*)\*/g, '$1<em>$2</em>');
  },

  md(text) {
    const lines = String(text || '').split('\n');
    const out = [];
    let i = 0;
    const isTableRow = l => /^\s*\|.*\|\s*$/.test(l);
    const cells = l => l.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim());

    while (i < lines.length) {
      const line = lines[i];
      const t = line.trim();

      if (!t) { i++; continue; }

      if (/^-{3,}$/.test(t)) { out.push('<hr class="my-4 border-slate-200">'); i++; continue; }

      let m;
      if ((m = t.match(/^(#{2,4})\s+(.*)$/))) {
        const size = m[1].length <= 3 ? 'text-base' : 'text-sm';
        out.push(`<h3 class="${size} font-bold text-slate-900 mt-5 mb-2">${this.mdInline(m[2])}</h3>`);
        i++; continue;
      }

      if (t.startsWith('>')) {
        const buf = [];
        while (i < lines.length && lines[i].trim().startsWith('>')) { buf.push(lines[i].trim().replace(/^>\s?/, '')); i++; }
        out.push(`<div class="my-3 p-3 rounded-lg bg-amber-50 border-l-4 border-amber-400 text-amber-950">${this.mdInline(buf.join(' '))}</div>`);
        continue;
      }

      if (isTableRow(line)) {
        const rows = [];
        while (i < lines.length && isTableRow(lines[i])) { rows.push(lines[i]); i++; }
        const body = rows.filter(r => !/^\s*\|[\s:|-]+\|\s*$/.test(r));
        const [head, ...rest] = body;
        out.push(`<div class="overflow-x-auto my-3"><table class="w-full text-left text-xs md:text-sm border border-slate-200 rounded-lg overflow-hidden">
          <thead class="bg-emerald-50 text-emerald-900"><tr>${cells(head).map(c => `<th class="px-3 py-2 font-semibold border-b border-slate-200">${this.mdInline(c)}</th>`).join('')}</tr></thead>
          <tbody>${rest.map(r => `<tr class="odd:bg-white even:bg-slate-50">${cells(r).map(c => `<td class="px-3 py-2 align-top border-b border-slate-100">${this.mdInline(c)}</td>`).join('')}</tr>`).join('')}</tbody>
        </table></div>`);
        continue;
      }

      if (/^(\s*)([-*]|\d+\.)\s+/.test(line)) {
        const items = [];
        const ordered = /^\s*\d+\./.test(line);
        while (i < lines.length && /^(\s*)([-*]|\d+\.)\s+/.test(lines[i])) {
          const indent = lines[i].match(/^(\s*)/)[1].length;
          const content = lines[i].replace(/^\s*([-*]|\d+\.)\s+/, '');
          items.push(`<li class="${indent >= 2 ? 'ml-5 list-[circle]' : ''}">${this.mdInline(content)}</li>`);
          i++;
        }
        out.push(ordered
          ? `<ol class="list-decimal pl-5 space-y-1 my-2">${items.join('')}</ol>`
          : `<ul class="list-disc pl-5 space-y-1 my-2">${items.join('')}</ul>`);
        continue;
      }

      const para = [];
      while (i < lines.length && lines[i].trim() && !/^(#{2,4}\s|>|\s*\||\s*([-*]|\d+\.)\s|-{3,}$)/.test(lines[i].trim())) {
        para.push(lines[i].trim()); i++;
      }
      if (para.length) out.push(`<p class="my-2">${this.mdInline(para.join(' '))}</p>`);
      else i++;
    }
    return out.join('\n');
  },

  navigateTo(viewName) {
    if (AppState.exam.inProgress && viewName !== 'exam') {
      if (!confirm('Tienes un simulacro en curso. Si sales ahora, el tiempo seguirá corriendo. ¿Deseas salir?')) {
        return;
      }
    }
    AppState.setView(viewName);
  },

  render() {
    const container = document.getElementById('main-content');
    if (!container) return;

    // Animar la entrada solo cuando cambia la pantalla, no en cada re-render
    // (seleccionar una opción o navegar con el teclado debe ser instantáneo).
    const viewKey = [
      AppState.activeView,
      AppState.exam.inProgress,
      AppState.selectedModule && AppState.selectedModule.id
    ].join('|');
    container.classList.toggle('no-enter', viewKey === this._lastViewKey);
    this._lastViewKey = viewKey;

    // Actualizar nav activa
    document.querySelectorAll('[data-nav]').forEach(el => {
      const v = el.getAttribute('data-nav');
      if (v === AppState.activeView || (AppState.activeView.startsWith('module') && v === 'modules')) {
        el.classList.add('bg-emerald-700', 'text-white');
        el.classList.remove('text-slate-200', 'hover:bg-emerald-800');
      } else {
        el.classList.remove('bg-emerald-700', 'text-white');
        el.classList.add('text-slate-200', 'hover:bg-emerald-800');
      }
    });

    // Renderizar vista correspondiente
    switch (AppState.activeView) {
      case 'dashboard':
        this.renderDashboard(container);
        break;
      case 'modules':
        this.renderModules(container);
        break;
      case 'module-study':
        this.renderModuleStudy(container);
        break;
      case 'exam':
        this.renderExam(container);
        break;
      case 'exam-result':
        this.renderExamResult(container);
        break;
      case 'flashcards':
        this.renderFlashcards(container);
        break;
      case 'documents':
        this.renderDocuments(container);
        break;
      case 'stats':
        this.renderStats(container);
        break;
      case 'ejes':
        this.renderEjes(container);
        break;
      default:
        this.renderDashboard(container);
    }
  },

  // -------------------------------------------------------------
  // 1. DASHBOARD / INICIO
  // -------------------------------------------------------------
  renderDashboard(container) {
    const c = AppState.convocatoria || {};
    const modulesCount = AppState.modules.length;

    container.innerHTML = `
      <div class="space-y-6 animate-fade-in">
        <!-- Banner Oficial Convocatoria -->
        <div class="panel-ink p-6 md:p-8">
          <div class="relative z-10 max-w-4xl">
            <div class="inline-flex items-center gap-2 px-3 py-1 bg-emerald-500/20 text-emerald-300 rounded-full text-xs font-semibold uppercase tracking-wider mb-3 border border-emerald-500/30">
              <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
              Convocatoria Oficial DIAN 2676 de 2024
            </div>
            <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight mb-2">
              Analista IV — Nivel Técnico (OPEC ${c.opec || '236799'})
            </h1>
            <p class="text-slate-300 text-sm md:text-base leading-relaxed mb-6">
              Ficha Manual de Funciones: <span class="text-emerald-400 font-medium">${c.ficha || 'CC-AU-2010'}</span>.
              Proceso de <span class="text-white font-medium">${c.subproceso || 'Cercanía con el ciudadano / Asistencia al usuario'}</span>.
              Compites por <span class="text-emerald-400 font-bold">${c.vacantes || 3} plazas</span> en Medellín, Tuluá y Arauca.
            </p>

            <!-- Grid de Pesos Oficiales -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-800/60 p-4 rounded-xl border border-slate-700/60">
              <div class="border-r border-slate-700/60 pr-2">
                <span class="text-xs text-rose-300 font-semibold uppercase block">Funcional (Eliminatoria)</span>
                <span class="text-xl font-black text-white">65%</span>
                <span class="text-[11px] text-rose-400 block">Mínimo 70.00/100</span>
              </div>
              <div class="border-r border-slate-700/60 pr-2">
                <span class="text-xs text-sky-300 font-semibold uppercase block">Comportamental</span>
                <span class="text-xl font-black text-white">15%</span>
                <span class="text-[11px] text-slate-400 block">Clasificatoria</span>
              </div>
              <div class="border-r border-slate-700/60 pr-2">
                <span class="text-xs text-amber-300 font-semibold uppercase block">Integridad</span>
                <span class="text-xl font-black text-white">10%</span>
                <span class="text-[11px] text-slate-400 block">Clasificatoria</span>
              </div>
              <div>
                <span class="text-xs text-emerald-300 font-semibold uppercase block">Antecedentes</span>
                <span class="text-xl font-black text-white">10%</span>
                <span class="text-[11px] text-slate-400 block">Hoja de vida</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Ruta de estudio por Ejes OPEC -->
        <div onclick="UI.navigateTo('ejes')" class="cursor-pointer bg-white rounded-2xl p-5 md:p-6 border border-slate-200 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="flex items-start gap-4">
            <div class="folio shrink-0 text-5xl leading-none text-emerald-700 w-14 text-center"><span class="hl not-italic">14</span></div>
            <div>
              <h2 class="text-lg font-black text-slate-900">Ruta de estudio por los 14 Ejes de tu OPEC</h2>
              <p class="text-xs md:text-sm text-slate-600">Qué estudiar según la ficha CC-AU-2010, lo que no puede faltar por eje, práctica dirigida y logística del día de la prueba.</p>
            </div>
          </div>
          <span class="shrink-0 px-5 py-2.5 bg-slate-900 text-white text-xs md:text-sm font-bold rounded-xl text-center">Abrir ruta de estudio →</span>
        </div>

        <!-- Tarjetas de Acceso Rápido -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <!-- Card Simulacro -->
          <div class="bg-white rounded-2xl p-6 shadow-md border border-slate-200/80 hover:shadow-lg transition-all flex flex-col justify-between">
            <div>
              <div class="w-12 h-12 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center mb-4">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 class="text-lg font-bold text-slate-800 mb-1">Simulacro Real</h2>
              <p class="text-slate-600 text-xs md:text-sm mb-4">
                Juicio Situacional con 3 opciones (A, B, C) y calificación con regla eliminatoria.
              </p>
            </div>
            <button onclick="UI.startExam()" class="w-full py-2.5 px-4 bg-rose-600 hover:bg-rose-700 text-white font-semibold rounded-xl transition text-center shadow-md shadow-rose-600/20 text-xs md:text-sm">
              Iniciar Simulacro
            </button>
          </div>

          <!-- Card Módulos -->
          <div class="bg-white rounded-2xl p-6 shadow-md border border-slate-200/80 hover:shadow-lg transition-all flex flex-col justify-between">
            <div>
              <div class="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-4">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h2 class="text-lg font-bold text-slate-800 mb-1">Módulos Teóricos</h2>
              <p class="text-slate-600 text-xs md:text-sm mb-4">
                ${modulesCount} módulos con ${AppState.modules.reduce((s, m) => s + m.topics_count, 0)} temas y ${AppState.modules.reduce((s, m) => s + m.questions_count, 0)} preguntas, alineados a los ejes de la OPEC.
              </p>
            </div>
            <button onclick="AppState.setView('modules')" class="w-full py-2.5 px-4 bg-emerald-700 hover:bg-emerald-800 text-white font-semibold rounded-xl transition text-center shadow-md shadow-emerald-700/20 text-xs md:text-sm">
              Explorar Temarios
            </button>
          </div>

          <!-- Card Flashcards -->
          <div class="bg-white rounded-2xl p-6 shadow-md border border-slate-200/80 hover:shadow-lg transition-all flex flex-col justify-between">
            <div>
              <div class="w-12 h-12 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center mb-4">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <h2 class="text-lg font-bold text-slate-800 mb-1">Flashcards</h2>
              <p class="text-slate-600 text-xs md:text-sm mb-4">
                Memoriza plazos de Ley 1755, suspensiones de RUT y recursos con tarjetas 3D.
              </p>
            </div>
            <button onclick="AppState.setView('flashcards')" class="w-full py-2.5 px-4 bg-amber-300 hover:bg-amber-400 text-amber-950 font-semibold rounded-xl transition text-center text-xs md:text-sm">
              Estudiar Tarjetas
            </button>
          </div>

          <!-- Card Biblioteca Normativa -->
          <div class="bg-white rounded-2xl p-6 shadow-md border border-slate-200/80 hover:shadow-lg transition-all flex flex-col justify-between">
            <div>
              <div class="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-4">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z" />
                </svg>
              </div>
              <h2 class="text-lg font-bold text-slate-800 mb-1">Normativa Oficial</h2>
              <p class="text-slate-600 text-xs md:text-sm mb-4">
                Decretos, leyes del Senado, Función Pública y guía de orientación de la CNSC.
              </p>
            </div>
            <button onclick="AppState.setView('documents')" class="w-full py-2.5 px-4 bg-indigo-700 hover:bg-indigo-800 text-white font-semibold rounded-xl transition text-center shadow-md shadow-indigo-700/20 text-xs md:text-sm">
              Ver Biblioteca →
            </button>
          </div>
        </div>

        <!-- Módulos Preview -->
        <div class="bg-white rounded-2xl p-6 shadow-md border border-slate-200/80">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-bold text-slate-800">Módulos Oficiales de la Convocatoria (${modulesCount})</h2>
            <button onclick="AppState.setView('modules')" class="text-sm font-semibold text-emerald-700 hover:text-emerald-800">
              Ver todos →
            </button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            ${AppState.modules.map(m => `
              <div onclick="UI.openModule(${m.id})" class="p-4 rounded-xl border border-slate-200 hover:border-emerald-500 hover:bg-emerald-50/30 cursor-pointer transition flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold px-2 py-0.5 rounded ${m.category === 'Funcional' ? 'bg-rose-100 text-rose-700' : 'bg-sky-100 text-sky-700'}">
                      Módulo ${m.number} • ${m.category}
                    </span>
                    <span class="text-xs text-slate-400 font-medium">${m.topics_count} temas</span>
                  </div>
                  <h3 class="font-bold text-slate-800 text-sm mb-1">${m.title}</h3>
                  <p class="text-xs text-slate-500 line-clamp-2">${m.subtitle || m.description}</p>
                </div>
                <div class="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-xs text-emerald-700 font-medium">
                  <span>${m.questions_count} preguntas de práctica</span>
                  <span>Estudiar →</span>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
  },

  // -------------------------------------------------------------
  // 2. LISTA DE MÓDULOS
  // -------------------------------------------------------------
  renderModules(container) {
    container.innerHTML = `
      <div class="space-y-6 animate-fade-in">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 class="text-2xl font-black text-slate-900">Módulos de Estudio Oficiales</h1>
            <p class="text-slate-500 text-sm">Contenido teórico y normativo según la Ficha CC-AU-2010 (Resolución 0067 de 2024)</p>
          </div>
          <button onclick="UI.startExam()" class="px-5 py-2.5 bg-rose-600 hover:bg-rose-700 text-white font-semibold rounded-xl transition shadow-md shadow-rose-600/20 text-sm">
            Iniciar Simulacro General
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          ${AppState.modules.map(m => `
            <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 hover:shadow-md transition flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between gap-2 mb-3">
                  <div class="flex items-center gap-2">
                    <span class="px-3 py-1 rounded-full text-xs font-bold ${
                      m.category === 'Funcional' ? 'bg-rose-100 text-rose-700 border border-rose-200' : 'bg-sky-100 text-sky-700 border border-sky-200'
                    }">
                      Módulo ${m.number} • ${m.category}
                    </span>
                    <span class="px-2.5 py-0.5 rounded text-xs font-semibold ${
                      m.priority === 'Máxima' ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-700'
                    }">
                      Prioridad ${m.priority}
                    </span>
                  </div>
                  <span class="text-xs text-slate-400 font-medium">${m.topics_count} Temas</span>
                </div>

                <h2 class="text-lg font-bold text-slate-900 mb-1">${m.title}</h2>
                <p class="text-xs font-medium text-emerald-700 mb-3">${m.subtitle || ''}</p>
                <p class="text-sm text-slate-600 leading-relaxed mb-4">${m.description || ''}</p>
              </div>

              <div class="pt-4 border-t border-slate-100 flex items-center justify-between">
                <div class="flex items-center gap-3 text-xs text-slate-500">
                  <span><b class="font-mono text-slate-700">${m.topics_count}</b> temas</span>
                  <span><b class="font-mono text-slate-700">${m.questions_count}</b> preguntas</span>
                  <span><b class="font-mono text-slate-700">${m.flashcards_count}</b> flashcards</span>
                </div>
                <button onclick="UI.openModule(${m.id})" class="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold rounded-lg transition shadow-sm">
                  Abrir Módulo →
                </button>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  },

  // -------------------------------------------------------------
  // 3. DETALLE DE MÓDULO (TEORÍA + PRÁCTICA)
  // -------------------------------------------------------------
  async openModule(moduleId) {
    try {
      AppState.selectedModule = await API.getModuleDetail(moduleId);
      AppState.moduleQuestions = await API.getModuleQuestions(moduleId);
      AppState.setView('module-study');
    } catch (err) {
      alert('Error al abrir el módulo: ' + err.message);
    }
  },

  renderModuleStudy(container) {
    const m = AppState.selectedModule;
    if (!m) {
      AppState.setView('modules');
      return;
    }

    container.innerHTML = `
      <div class="space-y-6 animate-fade-in">
        <!-- Navegación y Encabezado -->
        <div class="flex items-center justify-between">
          <button onclick="AppState.setView('modules')" class="text-sm font-semibold text-emerald-800 hover:text-emerald-950 flex items-center gap-1.5">
            ← Volver a Módulos
          </button>
          <span class="text-xs font-bold px-3 py-1 rounded-full ${m.category === 'Funcional' ? 'bg-rose-100 text-rose-700' : 'bg-sky-100 text-sky-700'}">
            Módulo ${m.number} • ${m.category}
          </span>
        </div>

        <div class="bg-white rounded-2xl p-6 md:p-8 shadow-sm border border-slate-200">
          <h1 class="text-2xl font-black text-slate-900 mb-2">${m.title}</h1>
          <p class="text-sm text-emerald-700 font-semibold mb-3">${m.subtitle || ''}</p>
          <p class="text-sm text-slate-600 mb-6">${m.description || ''}</p>

          <!-- Pestañas internas de estudio -->
          <div class="border-b border-slate-200 flex gap-4 mb-6">
            <button id="tab-theory-btn" onclick="UI.switchStudyTab('theory')" class="pb-3 border-b-2 border-emerald-700 font-bold text-sm text-emerald-800">
              Temario (${m.topics.length})
            </button>
            <button id="tab-practice-btn" onclick="UI.switchStudyTab('practice')" class="pb-3 border-b-2 border-transparent font-semibold text-sm text-slate-500 hover:text-slate-800">
              Práctica (${AppState.moduleQuestions.length})
            </button>
          </div>

          <!-- Contenido Teórico -->
          <div id="study-theory-content" class="space-y-6">
            ${m.topics.map(t => `
              <div class="p-5 md:p-6 bg-slate-50/70 rounded-xl border border-slate-200">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-3">
                  <h2 class="text-lg font-bold text-slate-900">${t.order}. ${t.title}</h2>
                  ${t.legal_basis ? `
                    <span class="inline-flex items-center text-xs font-mono font-medium text-emerald-800 bg-emerald-100/70 px-2.5 py-1 rounded border border-emerald-200">
                      ⚖️ ${t.legal_basis}
                    </span>
                  ` : ''}
                </div>
                <div class="text-sm text-slate-700 leading-relaxed max-w-none">
                  ${UI.md(t.content)}
                </div>
              </div>
            `).join('')}
          </div>

          <!-- Contenido Práctica -->
          <div id="study-practice-content" class="hidden space-y-6">
            ${AppState.moduleQuestions.length === 0 ? `
              <p class="text-slate-500 text-sm">No hay preguntas registradas para este módulo.</p>
            ` : AppState.moduleQuestions.map((q, idx) => `
              <div class="p-5 bg-slate-50 rounded-xl border border-slate-200">
                <div class="flex items-center justify-between mb-3">
                  <span class="text-xs font-bold text-slate-600">Pregunta ${idx + 1} de ${AppState.moduleQuestions.length}</span>
                  <span class="text-xs font-semibold px-2.5 py-0.5 rounded bg-emerald-100 text-emerald-800">${q.category}</span>
                </div>
                <div class="bg-white p-3.5 rounded-lg border border-slate-200 mb-3 text-xs md:text-sm text-slate-700 italic border-l-4 border-l-emerald-600">
                  <strong class="text-slate-900 not-italic block mb-1">Caso Situacional:</strong>
                  ${q.case_study}
                </div>
                <h3 class="text-sm font-bold text-slate-900 mb-3">${q.question_text}</h3>
                
                <div class="space-y-2 mb-4">
                  ${q.options.map(opt => `
                    <button onclick="UI.checkPracticeOption(${q.id}, ${opt.id}, ${opt.is_correct})" id="practice-opt-${opt.id}" class="w-full text-left p-3 rounded-lg border border-slate-200 hover:border-slate-300 bg-white text-xs md:text-sm text-slate-800 transition flex items-start gap-2.5">
                      <span class="font-bold text-slate-600 w-5">${opt.letter}.</span>
                      <span class="flex-1">${opt.text}</span>
                    </button>
                  `).join('')}
                </div>

                <div id="practice-feedback-${q.id}" class="hidden p-3.5 rounded-lg text-xs md:text-sm"></div>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
  },

  switchStudyTab(tab) {
    const theoryBtn = document.getElementById('tab-theory-btn');
    const practiceBtn = document.getElementById('tab-practice-btn');
    const theoryContent = document.getElementById('study-theory-content');
    const practiceContent = document.getElementById('study-practice-content');

    if (tab === 'theory') {
      theoryBtn.className = 'pb-3 border-b-2 border-emerald-700 font-bold text-sm text-emerald-800';
      practiceBtn.className = 'pb-3 border-b-2 border-transparent font-semibold text-sm text-slate-500 hover:text-slate-800';
      theoryContent.classList.remove('hidden');
      practiceContent.classList.add('hidden');
    } else {
      practiceBtn.className = 'pb-3 border-b-2 border-emerald-700 font-bold text-sm text-emerald-800';
      theoryBtn.className = 'pb-3 border-b-2 border-transparent font-semibold text-sm text-slate-500 hover:text-slate-800';
      practiceContent.classList.remove('hidden');
      theoryContent.classList.add('hidden');
    }
  },

  checkPracticeOption(questionId, optionId, isCorrect) {
    const feedbackBox = document.getElementById(`practice-feedback-${questionId}`);
    const q = AppState.moduleQuestions.find(x => x.id === questionId);

    // Resetear colores de opciones de esta pregunta
    q.options.forEach(opt => {
      const el = document.getElementById(`practice-opt-${opt.id}`);
      if (el) {
        el.className = 'w-full text-left p-3 rounded-lg border border-slate-200 bg-white text-xs md:text-sm text-slate-800 flex items-start gap-2.5';
      }
    });

    const selectedEl = document.getElementById(`practice-opt-${optionId}`);
    if (isCorrect) {
      if (selectedEl) selectedEl.className = 'w-full text-left p-3 rounded-lg border-2 border-emerald-600 bg-emerald-50 text-xs md:text-sm text-emerald-950 font-medium flex items-start gap-2.5';
      feedbackBox.className = 'p-3.5 rounded-lg text-xs md:text-sm bg-emerald-50 border border-emerald-200 text-emerald-900 block space-y-1';
      feedbackBox.innerHTML = `
        <div class="font-bold text-emerald-800">✅ ¡Correcto!</div>
        <div>${q.explanation}</div>
        ${q.legal_reference ? `<div class="text-xs text-emerald-700 font-mono mt-1">⚖️ Soporte: ${q.legal_reference}</div>` : ''}
      `;
    } else {
      if (selectedEl) selectedEl.className = 'w-full text-left p-3 rounded-lg border-2 border-rose-500 bg-rose-50 text-xs md:text-sm text-rose-950 flex items-start gap-2.5';
      // Resaltar la correcta
      const correctOpt = q.options.find(o => o.is_correct);
      if (correctOpt) {
        const cEl = document.getElementById(`practice-opt-${correctOpt.id}`);
        if (cEl) cEl.className = 'w-full text-left p-3 rounded-lg border-2 border-emerald-600 bg-emerald-50/60 text-xs md:text-sm text-slate-800 flex items-start gap-2.5';
      }
      feedbackBox.className = 'p-3.5 rounded-lg text-xs md:text-sm bg-rose-50 border border-rose-200 text-rose-900 block space-y-1';
      feedbackBox.innerHTML = `
        <div class="font-bold text-rose-800">❌ Incorrecto</div>
        <div>${q.explanation}</div>
        ${q.legal_reference ? `<div class="text-xs text-rose-700 font-mono mt-1">⚖️ Soporte: ${q.legal_reference}</div>` : ''}
      `;
    }
  },

  // -------------------------------------------------------------
  // 4. SIMULACRO REAL CRONOMETRADO (CNSC)
  // -------------------------------------------------------------
  // Abre la pantalla de configuración del simulacro
  openExamSetup() {
    if (AppState.exam.inProgress) { AppState.setView('exam'); return; }
    AppState.setView('exam');
  },

  setExamCount(n) {
    AppState.examConfig.count = n;
    this.render();
  },

  toggleExamModule(id) {
    const ids = AppState.examConfig.moduleIds;
    const idx = ids.indexOf(id);
    if (idx >= 0) ids.splice(idx, 1); else ids.push(id);
    this.render();
  },

  clearExamModules() {
    AppState.examConfig.moduleIds = [];
    this.render();
  },

  // Practicar un eje concreto: simulacro filtrado por sus módulos
  practiceEje(moduleIds, label) {
    this.startExam({ moduleIds, count: 15, label: label || 'Práctica por eje' });
  },

  repeatLastExam() {
    this.startExam(AppState.lastExamOpts || {});
  },

  async startExam(opts = {}) {
    if (AppState.exam.inProgress) {
      if (!confirm('Ya tienes un simulacro en curso. ¿Deseas descartarlo y empezar uno nuevo?')) {
        AppState.setView('exam');
        return;
      }
    }
    const cfg = AppState.examConfig;
    const count = opts.count !== undefined ? opts.count : cfg.count;
    const moduleIds = opts.moduleIds || cfg.moduleIds;
    try {
      const questions = await API.getExamQuestions({
        limit: count > 0 ? count : null,
        moduleIds,
        shuffle: true
      });
      if (!questions || questions.length === 0) {
        alert('No hay preguntas disponibles para el simulacro.');
        return;
      }
      AppState.resetExam();
      AppState.exam.questions = questions;
      AppState.exam.inProgress = true;
      AppState.exam.currentIndex = 0;
      AppState.exam.label = opts.label || (moduleIds.length ? 'Simulacro por módulos seleccionados' : 'Simulacro general');
      AppState.lastExamOpts = { count, moduleIds: [...moduleIds], label: AppState.exam.label };
      AppState.exam.remainingSeconds = Math.max(5 * 60, questions.length * cfg.secondsPerQuestion);

      // Iniciar timer
      AppState.exam.timerInterval = setInterval(() => {
        if (AppState.exam.remainingSeconds > 0) {
          AppState.exam.remainingSeconds--;
          AppState.exam.totalSecondsElapsed++;
          UI.updateExamTimerDisplay();
        } else {
          clearInterval(AppState.exam.timerInterval);
          alert('¡El tiempo ha finalizado! Se enviará tu simulacro para calificación.');
          UI.submitExam();
        }
      }, 1000);

      AppState.setView('exam');
    } catch (err) {
      alert('Error al iniciar simulacro: ' + err.message);
    }
  },

  renderExamSetupOptions() {
    const cfg = AppState.examConfig;
    const total = AppState.modules.reduce((s, m) => s + (m.questions_count || 0), 0);
    const selected = cfg.moduleIds;
    const pool = selected.length
      ? AppState.modules.filter(m => selected.includes(m.id)).reduce((s, m) => s + m.questions_count, 0)
      : total;
    const effective = cfg.count > 0 ? Math.min(cfg.count, pool) : pool;
    const minutes = Math.max(5, Math.round(effective * cfg.secondsPerQuestion / 60));
    const countBtn = (n, label) => `
      <button onclick="UI.setExamCount(${n})" class="px-3 py-2 rounded-lg text-xs font-bold border transition ${
        cfg.count === n ? 'bg-slate-900 text-white border-slate-900' : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
      }">${label}</button>`;

    return `
      <div class="text-left space-y-4">
        <div>
          <div class="text-xs font-bold text-slate-900 uppercase tracking-wider mb-2">1. Número de preguntas</div>
          <div class="flex flex-wrap gap-2">
            ${countBtn(20, '20 · rápido')}
            ${countBtn(40, '40 · estándar')}
            ${countBtn(60, '60 · intenso')}
            ${countBtn(0, `Todas (${pool})`)}
          </div>
        </div>
        <div>
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-bold text-slate-900 uppercase tracking-wider">2. Módulos (opcional)</span>
            ${selected.length ? `<button onclick="UI.clearExamModules()" class="text-xs font-semibold text-emerald-700 hover:underline">Usar todos</button>` : '<span class="text-xs text-slate-500">Todos incluidos</span>'}
          </div>
          <div class="flex flex-wrap gap-1.5">
            ${AppState.modules.map(m => `
              <button onclick="UI.toggleExamModule(${m.id})" class="px-2.5 py-1.5 rounded-lg text-[11px] font-semibold border transition ${
                selected.includes(m.id) ? 'bg-emerald-600 text-white border-emerald-700' : 'bg-white text-slate-600 border-slate-200 hover:border-emerald-400'
              }" title="${this.esc(m.title)}">M${m.number} · ${this.esc(m.title.length > 28 ? m.title.slice(0, 26) + '…' : m.title)} (${m.questions_count})</button>
            `).join('')}
          </div>
        </div>
        <div class="flex items-center justify-between bg-emerald-50 border border-emerald-200 rounded-xl px-4 py-3 text-sm">
          <span class="text-emerald-900"><strong>${effective}</strong> preguntas, balanceadas por módulo y en orden aleatorio</span>
          <span class="font-mono font-bold text-emerald-800">⏱ ${minutes} min</span>
        </div>
      </div>
    `;
  },

  updateExamTimerDisplay() {
    const timerEl = document.getElementById('exam-timer');
    if (!timerEl) return;
    const sec = AppState.exam.remainingSeconds;
    const h = Math.floor(sec / 3600);
    const m = Math.floor((sec % 3600) / 60).toString().padStart(2, '0');
    const s = (sec % 60).toString().padStart(2, '0');
    timerEl.innerText = h > 0 ? `${h}:${m}:${s}` : `${m}:${s}`;

    if (sec <= 300) {
      timerEl.className = 'font-mono text-base font-black px-3 py-1 rounded bg-rose-100 text-rose-700 border border-rose-300 animate-pulse';
    } else {
      timerEl.className = 'font-mono text-base font-black px-3 py-1 rounded bg-slate-100 text-slate-800 border border-slate-300';
    }
  },

  renderExam(container) {
    if (!AppState.exam.inProgress) {
      // Pantalla previa al inicio
      container.innerHTML = `
        <div class="max-w-2xl mx-auto bg-white rounded-2xl p-6 md:p-8 shadow-md border border-slate-200 text-center space-y-6 animate-fade-in">
          <div class="w-16 h-16 rounded-2xl bg-rose-50 text-rose-600 mx-auto flex items-center justify-center">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
          </div>
          <div>
            <h1 class="text-2xl font-black text-slate-900 mb-2">Simulacro Real Convocatoria DIAN 2676</h1>
            <p class="text-sm text-slate-600">Analista IV (OPEC 236799) • Asistencia al Usuario</p>
          </div>
          
          ${this.renderExamSetupOptions()}

          <div class="text-left bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs md:text-sm space-y-2 text-slate-700">
            <div class="font-bold text-slate-900 mb-1">Reglas Oficiales del Simulacro:</div>
            <p>• <strong>Metodología Juicio Situacional:</strong> Cada pregunta plantea un caso laboral realista con únicamente 3 opciones de respuesta (A, B y C).</p>
            <p>• <strong>Tiempo límite:</strong> ${Math.round(AppState.examConfig.secondsPerQuestion / 60)} minutos por pregunta (la prueba real dura 4 horas desde la orden de inicio).</p>
            <p>• <strong>Regla Eliminatoria:</strong> La Prueba Funcional tiene un peso del 65% y exige un puntaje mínimo aprobatorio de <strong>70.00 / 100</strong>. Obtener menos significa la eliminación inmediata del concurso.</p>
            <p>• <strong>Hoja de Respuestas:</strong> Podrás marcar preguntas para revisión y navegar libremente entre ellas antes de finalizar.</p>
            <p>• <strong>Teclado:</strong> <kbd class="px-1 border rounded bg-white">A</kbd> <kbd class="px-1 border rounded bg-white">B</kbd> <kbd class="px-1 border rounded bg-white">C</kbd> responden, <kbd class="px-1 border rounded bg-white">←</kbd> <kbd class="px-1 border rounded bg-white">→</kbd> navegan, <kbd class="px-1 border rounded bg-white">M</kbd> marca para revisión.</p>
          </div>

          <button onclick="UI.startExam()" class="w-full py-3.5 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-xl transition shadow-lg shadow-rose-600/30 text-base">
            Comenzar Simulacro Cronometrado
          </button>
        </div>
      `;
      return;
    }

    const ex = AppState.exam;
    const currentQ = ex.questions[ex.currentIndex];
    const totalQ = ex.questions.length;
    const isFlagged = ex.flagged.has(currentQ.id);
    const selectedOptionId = ex.answers[currentQ.id];

    container.innerHTML = `
      <div class="space-y-6 animate-fade-in">
        <!-- Barra Superior de Control -->
        <div class="bg-white rounded-2xl p-4 shadow-sm border border-slate-200 flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center gap-3">
            <span class="text-xs text-slate-500 font-bold uppercase tracking-wider">Tiempo Restante:</span>
            <div id="exam-timer" class="font-mono text-base font-black px-3 py-1 rounded bg-slate-100 text-slate-800 border border-slate-300">
              --:--
            </div>
          </div>

          <div class="flex items-center gap-2">
            <button onclick="UI.toggleFlagQuestion(${currentQ.id})" class="px-3 py-1.5 rounded-lg text-xs font-semibold border transition flex items-center gap-1 ${
              isFlagged ? 'bg-amber-100 border-amber-300 text-amber-900' : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
            }">
              <span>${isFlagged ? '★ Marcada para revisión' : '☆ Marcar para revisar'}</span>
            </button>
            <button onclick="UI.confirmSubmitExam()" class="px-4 py-1.5 bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold rounded-lg transition shadow-sm">
              Finalizar y Calificar
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <!-- Columna Principal: Pregunta -->
          <div class="lg:col-span-3 bg-white rounded-2xl p-6 md:p-8 shadow-sm border border-slate-200 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-bold px-3 py-1 rounded-full ${
                  currentQ.category === 'Funcional' ? 'bg-rose-100 text-rose-700' :
                  currentQ.category === 'Comportamental' ? 'bg-sky-100 text-sky-700' : 'bg-amber-100 text-amber-800'
                }">
                  Prueba ${currentQ.category}
                </span>
                <span class="text-xs font-medium text-slate-500">Pregunta ${ex.currentIndex + 1} de ${totalQ}</span>
              </div>

              <!-- Caso Situacional -->
              <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 mb-5 text-slate-800 text-xs md:text-sm leading-relaxed border-l-4 border-l-rose-500">
                <span class="font-bold text-slate-900 block mb-1 text-xs uppercase tracking-wider text-rose-700">Caso Laboral (Situación DIAN):</span>
                ${currentQ.case_study}
              </div>

              <!-- Enunciado -->
              <h2 class="text-base md:text-lg font-bold text-slate-900 mb-5 leading-snug">
                ${currentQ.question_text}
              </h2>

              <!-- Opciones A, B, C estrictas -->
              <div class="space-y-3 mb-6">
                ${currentQ.options.map(opt => {
                  const isSelected = selectedOptionId === opt.id;
                  return `
                    <label onclick="UI.selectExamOption(${currentQ.id}, ${opt.id})" class="cursor-pointer block p-4 rounded-xl border transition ${
                      isSelected
                        ? 'border-2 border-emerald-600 bg-emerald-50/70 shadow-sm'
                        : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                    }">
                      <div class="flex items-start gap-3">
                        <div class="w-6 h-6 rounded-full flex items-center justify-center font-bold text-xs ${
                          isSelected ? 'bg-emerald-600 text-white' : 'bg-slate-200 text-slate-700'
                        }">
                          ${opt.letter}
                        </div>
                        <div class="flex-1 text-xs md:text-sm text-slate-800 leading-relaxed pt-0.5">
                          ${opt.text}
                        </div>
                      </div>
                    </label>
                  `;
                }).join('')}
              </div>
            </div>

            <!-- Navegación Pregunta -->
            <div class="pt-4 border-t border-slate-100 flex items-center justify-between">
              <button onclick="UI.prevExamQuestion()" ${ex.currentIndex === 0 ? 'disabled' : ''} class="px-4 py-2 rounded-lg text-xs font-bold border border-slate-200 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed">
                ← Anterior
              </button>
              <span class="text-xs text-slate-400">Selecciona tu opción para guardar automáticamente</span>
              <button onclick="UI.nextExamQuestion()" ${ex.currentIndex === totalQ - 1 ? 'disabled' : ''} class="px-4 py-2 rounded-lg text-xs font-bold bg-slate-900 text-white hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed">
                Siguiente →
              </button>
            </div>
          </div>

          <!-- Columna Lateral: Hoja de Respuestas -->
          <div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-200">
            <h3 class="font-bold text-slate-800 text-sm mb-3">Hoja de Respuestas</h3>
            <div class="grid grid-cols-4 sm:grid-cols-6 lg:grid-cols-4 gap-2 mb-4">
              ${ex.questions.map((q, idx) => {
                const hasAnswer = ex.answers[q.id] !== undefined;
                const isF = ex.flagged.has(q.id);
                const isCurrent = ex.currentIndex === idx;

                let btnClass = 'bg-slate-100 text-slate-600 border-slate-200';
                if (hasAnswer) btnClass = 'bg-emerald-600 text-white border-emerald-700';
                if (isF) btnClass = 'bg-amber-400 text-amber-950 font-black border-amber-500';
                if (isCurrent) btnClass += ' ring-2 ring-offset-2 ring-slate-900';

                return `
                  <button onclick="UI.goToExamQuestion(${idx})" class="w-full aspect-square rounded-lg text-xs font-bold border transition flex items-center justify-center ${btnClass}">
                    ${idx + 1}
                  </button>
                `;
              }).join('')}
            </div>

            <div class="space-y-1.5 text-[11px] text-slate-500 border-t border-slate-100 pt-3">
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded bg-emerald-600"></span>
                <span>Respondida</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded bg-amber-400"></span>
                <span>Marcada para revisión</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded bg-slate-100 border border-slate-200"></span>
                <span>Sin responder</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    this.updateExamTimerDisplay();
  },

  selectExamOption(questionId, optionId) {
    AppState.exam.answers[questionId] = optionId;
    this.render();
  },

  toggleFlagQuestion(questionId) {
    if (AppState.exam.flagged.has(questionId)) {
      AppState.exam.flagged.delete(questionId);
    } else {
      AppState.exam.flagged.add(questionId);
    }
    this.render();
  },

  prevExamQuestion() {
    if (AppState.exam.currentIndex > 0) {
      AppState.exam.currentIndex--;
      this.render();
    }
  },

  nextExamQuestion() {
    if (AppState.exam.currentIndex < AppState.exam.questions.length - 1) {
      AppState.exam.currentIndex++;
      this.render();
    }
  },

  goToExamQuestion(idx) {
    AppState.exam.currentIndex = idx;
    this.render();
  },

  confirmSubmitExam() {
    const answeredCount = Object.keys(AppState.exam.answers).length;
    const totalCount = AppState.exam.questions.length;
    const remaining = totalCount - answeredCount;

    let msg = `Has respondido ${answeredCount} de ${totalCount} preguntas.`;
    if (remaining > 0) {
      msg += ` Tienes ${remaining} preguntas sin responder.`;
    }
    msg += '\n\n¿Estás seguro de enviar tu examen para calificación oficial?';

    if (confirm(msg)) {
      this.submitExam();
    }
  },

  async submitExam() {
    clearInterval(AppState.exam.timerInterval);
    const ex = AppState.exam;
    const answersList = ex.questions.map(q => ({
      question_id: q.id,
      selected_option_id: ex.answers[q.id] || null
    }));

    try {
      const result = await API.submitExam(answersList, ex.totalSecondsElapsed);
      AppState.exam.lastResult = result;
      AppState.exam.inProgress = false;
      AppState.setView('exam-result');
    } catch (err) {
      alert('Error al calificar examen: ' + err.message);
    }
  },

  // -------------------------------------------------------------
  // 5. RESULTADOS Y RETROALIMENTACIÓN DETALLADA
  // -------------------------------------------------------------
  renderExamResult(container) {
    const r = AppState.exam.lastResult;
    if (!r) {
      AppState.setView('dashboard');
      return;
    }

    const passed = r.passed_functional;
    this._onlyWrong = false;

    container.innerHTML = `
      <div class="space-y-6 animate-fade-in">
        <!-- Veredicto Principal -->
        <div class="p-6 md:p-8 ${
          passed ? 'panel-ink is-pass' : 'panel-ink is-fail'
        }">
          <div class="max-w-3xl">
            <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider mb-3 ${
              passed ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-400/30' : 'bg-rose-500/20 text-rose-300 border border-rose-400/30'
            }">
              ${passed ? '✓ CLASIFICADO EN PRUEBA ELIMINATORIA' : '✕ NO ALCANZÓ UMBRAL ELIMINATORIO'}
            </div>
            <h1 class="text-2xl md:text-3xl font-black mb-2">
              ${passed ? '¡Aprobaste la Prueba Funcional!' : 'Eliminado del Proceso de Selección'}
            </h1>
            <p class="text-sm md:text-base text-slate-200 mb-6 leading-relaxed">
              ${r.status_message}
            </p>

            <!-- Resumen de Puntajes -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-black/30 p-4 rounded-xl border border-white/10">
              <div>
                <span class="text-[11px] text-slate-300 uppercase block font-medium">Funcional (65%)</span>
                <span class="text-2xl font-black ${r.functional_score >= 70 ? 'text-emerald-400' : 'text-rose-400'}">
                  ${r.functional_score.toFixed(1)}
                </span>
                <span class="text-[10px] text-slate-400 block">Min: 70.00</span>
              </div>
              <div>
                <span class="text-[11px] text-slate-300 uppercase block font-medium">Comportamental (15%)</span>
                <span class="text-2xl font-black text-sky-400">${r.behavioral_score.toFixed(1)}</span>
                <span class="text-[10px] text-slate-400 block">Sobre 100</span>
              </div>
              <div>
                <span class="text-[11px] text-slate-300 uppercase block font-medium">Integridad (10%)</span>
                <span class="text-2xl font-black text-amber-400">${r.integrity_score.toFixed(1)}</span>
                <span class="text-[10px] text-slate-400 block">Sobre 100</span>
              </div>
              <div>
                <span class="text-[11px] text-slate-300 uppercase block font-medium">Puntaje Ponderado</span>
                <span class="text-2xl font-black text-white">${r.total_weighted_score.toFixed(2)}</span>
                <span class="text-[10px] text-slate-400 block">Escrito (Max 90)</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Desglose por Módulos -->
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-200">
          <h2 class="text-lg font-bold text-slate-900 mb-4">Desempeño por Módulo Oficial</h2>
          <div class="space-y-3">
            ${Object.entries(r.module_breakdown).map(([modName, data]) => `
              <div>
                <div class="flex items-center justify-between text-xs md:text-sm font-semibold text-slate-700 mb-1">
                  <span>${modName}</span>
                  <span>${data.correct} de ${data.total} (${data.percentage}%)</span>
                </div>
                <div class="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                  <div class="h-2.5 rounded-full ${data.percentage >= 70 ? 'bg-emerald-600' : 'bg-rose-500'}" style="width: ${data.percentage}%"></div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Revisión Pregunta por Pregunta -->
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-bold text-slate-900">Revisión Pedagógica y Normativa</h2>
            <div class="flex gap-2">
              <button onclick="UI.reviewWrongOnly()" class="px-4 py-2 bg-white border border-slate-300 hover:bg-slate-50 text-slate-800 font-bold text-xs rounded-xl transition">
                Ver solo mis errores
              </button>
              <button onclick="UI.repeatLastExam()" class="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs rounded-xl transition shadow">
                Intentar Nuevo Simulacro
              </button>
            </div>
          </div>

          ${r.questions_review.map((item, idx) => `
            <div data-review-correct="${item.is_correct}" class="bg-white rounded-2xl p-6 shadow-sm border ${item.is_correct ? 'border-emerald-200' : 'border-rose-200'}">
              <div class="flex items-center justify-between mb-3">
                <span class="text-xs font-bold px-2.5 py-0.5 rounded ${item.is_correct ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}">
                  ${item.is_correct ? '✓ Correcta' : '✕ Incorrecta'} • Pregunta ${idx + 1}
                </span>
                <span class="text-xs font-semibold text-slate-500">${item.category}</span>
              </div>

              <!-- Caso -->
              <div class="bg-slate-50 p-3.5 rounded-lg border border-slate-200 text-xs md:text-sm text-slate-700 mb-3 italic">
                <strong class="text-slate-900 not-italic block mb-0.5">Caso Laboral:</strong>
                ${item.case_study}
              </div>

              <h3 class="text-sm font-bold text-slate-900 mb-3">${item.question_text}</h3>

              <!-- Opciones -->
              <div class="space-y-2 mb-4">
                ${item.options.map(opt => {
                  let optStyle = 'border-slate-200 bg-white text-slate-700';
                  if (opt.id === item.correct_option_id) {
                    optStyle = 'border-2 border-emerald-600 bg-emerald-50 text-emerald-950 font-bold';
                  } else if (opt.id === item.selected_option_id && !item.is_correct) {
                    optStyle = 'border-2 border-rose-500 bg-rose-50 text-rose-950';
                  }
                  return `
                    <div class="p-3 rounded-lg border text-xs md:text-sm flex items-start gap-2.5 ${optStyle}">
                      <span class="font-bold w-5">${opt.letter}.</span>
                      <span class="flex-1">${opt.text}</span>
                      ${opt.id === item.correct_option_id ? '<span class="text-emerald-700 font-bold text-xs">Clave Oficial</span>' : ''}
                      ${opt.id === item.selected_option_id && !item.is_correct ? '<span class="text-rose-700 font-bold text-xs">Tu Respuesta</span>' : ''}
                    </div>
                  `;
                }).join('')}
              </div>

              <!-- Retroalimentación con Fundamento -->
              <div class="p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl text-xs md:text-sm space-y-1.5">
                <div class="font-bold text-emerald-900">Justificación Técnica de la Clave:</div>
                <p class="text-slate-800 leading-relaxed">${item.explanation}</p>
                ${item.legal_reference ? `
                  <div class="font-mono text-xs text-emerald-800 font-semibold pt-1">
                    ⚖️ Marco Legal: ${item.legal_reference}
                  </div>
                ` : ''}
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  },

  reviewWrongOnly() {
    this._onlyWrong = !this._onlyWrong;
    document.querySelectorAll('[data-review-correct="true"]').forEach(el => {
      el.classList.toggle('hidden', this._onlyWrong);
    });
  },

  // -------------------------------------------------------------
  // 6. FLASHCARDS INTERACTIVAS (MEMORIZACIÓN DE PLAZOS)
  // -------------------------------------------------------------
  async renderFlashcards(container) {
    if (AppState.flashcards.items.length === 0) {
      try {
        const sel = AppState.flashcards.selectedModuleId;
        AppState.flashcards.items = await API.getFlashcards(sel === 'all' ? null : sel);
        AppState.flashcards.currentIndex = 0;
        AppState.flashcards.isFlipped = false;
      } catch (err) {
        console.error(err);
      }
    }

    const fc = AppState.flashcards;
    const currentCard = fc.items[fc.currentIndex];

    container.innerHTML = `
      <div class="max-w-2xl mx-auto space-y-6 animate-fade-in">
        <div class="text-center">
          <h1 class="text-2xl font-black text-slate-900">Flashcards de Alto Rendimiento</h1>
          <p class="text-xs md:text-sm text-slate-500">Memoriza términos perentorios, plazos de Ley 1755, suspensiones de RUT y competencias</p>
        </div>

        <div class="flex flex-col sm:flex-row gap-2 items-stretch sm:items-center justify-between">
          <select onchange="UI.filterFlashcards(this.value)" class="flex-1 px-3 py-2 rounded-xl border border-slate-200 bg-white text-xs md:text-sm font-semibold text-slate-700">
            <option value="all" ${fc.selectedModuleId === 'all' ? 'selected' : ''}>Todos los módulos</option>
            ${AppState.modules.map(m => `<option value="${m.id}" ${String(fc.selectedModuleId) === String(m.id) ? 'selected' : ''}>Módulo ${m.number} · ${this.esc(m.title)} (${m.flashcards_count})</option>`).join('')}
          </select>
          <button onclick="UI.shuffleFlashcards()" class="px-4 py-2 rounded-xl border border-slate-200 bg-white text-xs font-bold text-slate-700 hover:bg-slate-50">Barajar</button>
        </div>

        ${!currentCard ? `
          <div class="text-center p-8 bg-white rounded-2xl border border-slate-200">
            <p class="text-slate-500 text-sm">No hay flashcards disponibles.</p>
          </div>
        ` : `
          <!-- Tarjeta con Efecto Flip -->
          <div class="perspective-1000 w-full h-96 cursor-pointer" onclick="UI.toggleFlipFlashcard()">
            <div id="flashcard-inner" class="relative w-full h-full transition-card transform-style-3d ${fc.isFlipped ? 'rotate-y-180' : ''}">
              
              <!-- Lado Frontal (Término / Pregunta) -->
              <div class="absolute inset-0 w-full h-full backface-hidden bg-white rounded-3xl p-8 shadow-md border-2 border-emerald-600/30 flex flex-col justify-between text-center select-none">
                <div class="flex items-center justify-between text-xs font-bold text-slate-400">
                  <span class="px-3 py-1 bg-emerald-50 text-emerald-700 rounded-full font-semibold">${currentCard.category}</span>
                  <span>${fc.currentIndex + 1} de ${fc.items.length}</span>
                </div>
                <div class="my-auto">
                  <span class="text-xs text-emerald-600 font-bold uppercase tracking-wider block mb-2">Término o Pregunta</span>
                  <h2 class="text-xl md:text-2xl font-black text-slate-900 leading-snug">${currentCard.term}</h2>
                </div>
                <div class="text-xs text-slate-400 font-medium">
                  Toca la tarjeta para ver la respuesta y norma →
                </div>
              </div>

              <!-- Lado Trasero (Definición / Plazo / Norma) -->
              <div class="absolute inset-0 w-full h-full backface-hidden rotate-y-180 bg-slate-900 rounded-3xl p-8 shadow-xl border-2 border-emerald-500 text-white flex flex-col justify-between text-center select-none">
                <div class="flex items-center justify-between text-xs font-bold text-emerald-400">
                  <span>Respuesta Oficial</span>
                  <span>${fc.currentIndex + 1} de ${fc.items.length}</span>
                </div>
                <div class="my-auto space-y-3 overflow-y-auto">
                  <p class="text-sm md:text-base font-medium text-slate-100 leading-relaxed">${currentCard.definition}</p>
                  ${currentCard.legal_norm ? `
                    <div class="inline-block px-3 py-1 bg-emerald-500/20 text-emerald-300 rounded-lg text-xs font-mono font-semibold border border-emerald-500/30">
                      ⚖️ ${currentCard.legal_norm}
                    </div>
                  ` : ''}
                </div>
                <div class="text-xs text-slate-400">
                  Toca para volver a voltear
                </div>
              </div>

            </div>
          </div>

          <!-- Controles de Navegación -->
          <div class="flex items-center justify-between gap-4">
            <button onclick="UI.prevFlashcard()" class="px-5 py-2.5 rounded-xl border border-slate-200 bg-white font-bold text-xs text-slate-700 hover:bg-slate-50 transition shadow-sm">
              ← Anterior
            </button>
            <button onclick="UI.toggleFlipFlashcard()" class="px-6 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs rounded-xl transition shadow-md shadow-emerald-700/20">
              Girar Tarjeta (Espacio)
            </button>
            <button onclick="UI.nextFlashcard()" class="px-5 py-2.5 rounded-xl border border-slate-200 bg-white font-bold text-xs text-slate-700 hover:bg-slate-50 transition shadow-sm">
              Siguiente →
            </button>
          </div>
        `}
      </div>
    `;
  },

  filterFlashcards(moduleId) {
    const fc = AppState.flashcards;
    fc.selectedModuleId = moduleId;
    fc.items = [];
    fc.currentIndex = 0;
    fc.isFlipped = false;
    this.render();
  },

  shuffleFlashcards() {
    const fc = AppState.flashcards;
    for (let i = fc.items.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [fc.items[i], fc.items[j]] = [fc.items[j], fc.items[i]];
    }
    fc.currentIndex = 0;
    fc.isFlipped = false;
    this.render();
  },

  toggleFlipFlashcard() {
    AppState.flashcards.isFlipped = !AppState.flashcards.isFlipped;
    const cardEl = document.getElementById('flashcard-inner');
    if (cardEl) {
      if (AppState.flashcards.isFlipped) {
        cardEl.classList.add('rotate-y-180');
      } else {
        cardEl.classList.remove('rotate-y-180');
      }
    }
  },

  prevFlashcard() {
    const fc = AppState.flashcards;
    if (fc.currentIndex > 0) {
      fc.currentIndex--;
      fc.isFlipped = false;
      this.render();
    }
  },

  nextFlashcard() {
    const fc = AppState.flashcards;
    if (fc.currentIndex < fc.items.length - 1) {
      fc.currentIndex++;
      fc.isFlipped = false;
      this.render();
    }
  },

  // -------------------------------------------------------------
  // 6b. RUTA DE ESTUDIO POR EJES TEMÁTICOS OPEC
  // -------------------------------------------------------------
  getStudiedEjes() {
    try { return new Set(JSON.parse(localStorage.getItem('prepdian.ejesEstudiados') || '[]')); }
    catch (e) { return new Set(); }
  },

  toggleEjeStudied(num) {
    const set = this.getStudiedEjes();
    if (set.has(num)) set.delete(num); else set.add(num);
    try { localStorage.setItem('prepdian.ejesEstudiados', JSON.stringify([...set])); } catch (e) { /* sin almacenamiento */ }
    this.render();
  },

  countdownText(iso) {
    const diff = new Date(iso).getTime() - Date.now();
    if (isNaN(diff)) return '';
    if (diff <= 0) return '¡Hoy es la prueba! Mucha suerte 🍀';
    const h = Math.floor(diff / 3600000);
    const d = Math.floor(h / 24);
    const rh = h % 24;
    const m = Math.floor((diff % 3600000) / 60000);
    return d > 0 ? `Faltan ${d} d ${rh} h ${m} min` : `Faltan ${rh} h ${m} min`;
  },

  async renderEjes(container) {
    if (!AppState.ejes) {
      container.innerHTML = `<div class="h-40 bg-slate-200 rounded-2xl animate-pulse"></div>`;
      try {
        AppState.ejes = await API.getEjes();
      } catch (err) {
        container.innerHTML = `<p class="text-rose-700 text-sm">No se pudieron cargar los ejes: ${this.esc(err.message)}</p>`;
        return;
      }
      if (AppState.activeView !== 'ejes') return;
    }
    const data = AppState.ejes;
    const studied = this.getStudiedEjes();
    const total = data.ejes.length;
    const done = data.ejes.filter(e => studied.has(e.numero)).length;
    const pct = Math.round((done / total) * 100);
    const grupos = [...new Set(data.ejes.map(e => e.grupo))];
    const groupStyle = {
      'Propia del empleo': 'bg-rose-100 text-rose-800 border-rose-200',
      'Básica / común': 'bg-emerald-100 text-emerald-800 border-emerald-200',
      'Pruebas Comportamental e Integridad': 'bg-sky-100 text-sky-800 border-sky-200'
    };

    container.innerHTML = `
      <div class="space-y-6 animate-fade-in">
        <!-- Encabezado + cuenta regresiva -->
        <div class="panel-ink p-6 md:p-8">
          <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
              <div class="text-xs font-semibold uppercase tracking-wider text-emerald-300 mb-2">Ficha CC-AU-2010 · OPEC 236799</div>
              <h1 class="text-2xl md:text-3xl font-extrabold mb-1">Ruta de estudio por Ejes Temáticos</h1>
              <p class="text-slate-300 text-sm max-w-2xl">Los 14 ejes que la CNSC evalúa para tu empleo, cada uno con lo que no puede faltar y sus módulos de estudio, práctica y flashcards.</p>
            </div>
            <div class="bg-black/30 border border-white/10 rounded-xl px-4 py-3 text-center min-w-[220px]">
              <div class="text-[11px] uppercase tracking-wider text-slate-300">Prueba escrita · dom. 8 nov 2026</div>
              <div id="ejes-countdown" class="text-lg font-black text-amber-300">${this.countdownText(data.fecha_prueba)}</div>
            </div>
          </div>
          <div class="mt-5">
            <div class="flex justify-between text-xs text-slate-300 mb-1">
              <span>Tu repaso: ${done} de ${total} ejes marcados como estudiados</span><span>${pct}%</span>
            </div>
            <div class="w-full h-2.5 bg-white/10 rounded-full overflow-hidden">
              <div class="bar-fill h-2.5 bg-amber-300 rounded-full" style="transform:scaleX(${pct/100})"></div>
            </div>
          </div>
        </div>

        <!-- Logística del día -->
        <details class="bg-white rounded-2xl p-5 shadow-sm border border-amber-200 group" ${done === 0 ? 'open' : ''}>
          <summary class="cursor-pointer font-bold text-slate-900 text-sm flex items-center justify-between">
            <span class="font-display text-base">Lo que dice la Guía de Orientación <span class="text-slate-500 font-sans text-xs">· léelo hoy</span></span>
            <span class="text-xs text-slate-400 group-open:hidden">ver</span>
          </summary>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mt-4 text-xs md:text-sm text-slate-700">
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-200"><strong>Horario:</strong> apertura de puertas 7:15 a. m., inicio 8:00 a. m., <strong>cierre de puertas 8:30 a. m.</strong> (quien llegue después queda ausente). Duración: <strong>4 horas</strong>.</div>
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-200"><strong>Hoja de respuestas:</strong> solo se califica lo marcado en la hoja, con <strong>lápiz de mina negra N.º 2</strong>; lo escrito en el cuadernillo no cuenta.</div>
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-200"><strong>Corte normativo:</strong> ${this.esc(data.corte_normativo)}. La Ley 2586 de 2026 (régimen sancionatorio aduanero) queda por fuera.</div>
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-200"><strong>Funcional (65 %):</strong> juicio situacional, 3 opciones (A, B, C), una correcta. Eliminatoria: mínimo <strong>70/100</strong>.</div>
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-200"><strong>Comportamental (15 %) e Integridad (10 %):</strong> escala Likert de 4 opciones con 2 subescalas de control. Responde con consistencia, sin marcar extremos por reflejo.</div>
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-200"><strong>Citación:</strong> confirma en SIMO tu ciudad, sitio y salón. Lleva tu documento de identidad original.</div>
          </div>
          <p class="text-[11px] text-slate-400 mt-3">Fuente: Guía de Orientación al Aspirante DIAN 2676 (CNSC – Areandina). Confirma siempre los datos en tu citación de SIMO.</p>
        </details>

        ${grupos.map(g => `
          <div>
            <h2 class="text-sm font-black uppercase tracking-wider text-slate-500 mb-3">${this.esc(g)}</h2>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
              ${data.ejes.filter(e => e.grupo === g).map(e => {
                const isDone = studied.has(e.numero);
                const modIds = JSON.stringify(e.modulos.map(m => m.id));
                return `
                <div class="bg-white rounded-2xl p-5 shadow-sm border ${isDone ? 'border-emerald-400 ring-1 ring-emerald-200' : 'border-slate-200'} flex flex-col">
                  <div class="flex items-start justify-between gap-3 mb-3">
                    <div class="flex items-start gap-3">
                      <span class="folio shrink-0 w-9 h-9 rounded-xl flex items-center justify-center text-lg border ${groupStyle[g] || 'bg-slate-100 text-slate-700 border-slate-200'}">${e.numero}</span>
                      <h3 class="font-bold text-slate-900 text-sm md:text-base leading-snug">${this.esc(e.titulo)}</h3>
                    </div>
                    <label class="shrink-0 flex items-center gap-1.5 text-[11px] font-semibold cursor-pointer select-none ${isDone ? 'text-emerald-700' : 'text-slate-400'}">
                      <input type="checkbox" ${isDone ? 'checked' : ''} onchange="UI.toggleEjeStudied(${e.numero})" class="w-4 h-4 accent-emerald-600">
                      Estudiado
                    </label>
                  </div>
                  <ul class="space-y-1.5 text-xs md:text-sm text-slate-700 mb-4 flex-1">
                    ${e.claves.map(c => `<li class="flex gap-2"><span class="text-emerald-600 font-bold">✓</span><span>${this.esc(c)}</span></li>`).join('')}
                  </ul>
                  <div class="flex flex-wrap items-center gap-2 pt-3 border-t border-slate-100">
                    ${e.modulos.map(m => `
                      <button onclick="UI.openModule(${m.id})" class="px-2.5 py-1.5 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-800 text-[11px] font-bold border border-emerald-200">M${m.number} · ${this.esc(m.title.length > 30 ? m.title.slice(0, 28) + '…' : m.title)}</button>
                    `).join('')}
                    <button onclick='UI.practiceEje(${modIds}, ${JSON.stringify('Práctica · Eje ' + e.numero).replace(/'/g, '&#39;')})' class="ml-auto px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-700 text-white text-[11px] font-bold">Practicar · ${e.questions_count}</button>
                  </div>
                </div>`;
              }).join('')}
            </div>
          </div>
        `).join('')}
      </div>
    `;

    clearInterval(this._countdownTimer);
    this._countdownTimer = setInterval(() => {
      const el = document.getElementById('ejes-countdown');
      if (!el) { clearInterval(this._countdownTimer); return; }
      el.textContent = this.countdownText(data.fecha_prueba);
    }, 30000);
  },

  // -------------------------------------------------------------
  // 7. ESTADÍSTICAS Y PROGRESO
  // -------------------------------------------------------------
  async renderStats(container) {
    try {
      const stats = await API.getExamStatistics();
      container.innerHTML = `
        <div class="space-y-6 animate-fade-in">
          <div>
            <h1 class="text-2xl font-black text-slate-900">Historial y Estadísticas de Preparación</h1>
            <p class="text-xs md:text-sm text-slate-500">Métricas acumuladas de tus simulacros cronometrados</p>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
              <span class="text-xs text-slate-400 font-bold uppercase block">Simulacros Realizados</span>
              <span class="text-2xl font-black text-slate-900">${stats.total_attempts}</span>
            </div>
            <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
              <span class="text-xs text-slate-400 font-bold uppercase block">Tasa de Aprobación</span>
              <span class="text-2xl font-black ${stats.pass_rate >= 70 ? 'text-emerald-600' : 'text-rose-600'}">${stats.pass_rate}%</span>
            </div>
            <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
              <span class="text-xs text-slate-400 font-bold uppercase block">Promedio Funcional</span>
              <span class="text-2xl font-black text-slate-900">${stats.avg_functional_score}</span>
              <span class="text-[11px] text-slate-400 block">Min: 70.00</span>
            </div>
            <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
              <span class="text-xs text-slate-400 font-bold uppercase block">Puntaje Más Alto</span>
              <span class="text-2xl font-black text-emerald-600">${stats.highest_score}</span>
            </div>
          </div>

          <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-200">
            <h2 class="text-lg font-bold text-slate-900 mb-4">Historial de Intentos</h2>
            ${stats.recent_history.length === 0 ? `
              <p class="text-sm text-slate-500 py-4 text-center">Aún no has completado simulacros. Inicia tu primer intento para medir tus resultados.</p>
            ` : `
              <div class="overflow-x-auto">
                <table class="w-full text-left text-xs md:text-sm">
                  <thead class="bg-slate-50 text-slate-600 uppercase text-[11px] border-b border-slate-200">
                    <tr>
                      <th class="py-3 px-4">Fecha y Hora</th>
                      <th class="py-3 px-4">Aciertos</th>
                      <th class="py-3 px-4">Prueba Funcional</th>
                      <th class="py-3 px-4">Puntaje Ponderado</th>
                      <th class="py-3 px-4">Estado</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100">
                    ${stats.recent_history.map(h => `
                      <tr class="hover:bg-slate-50/60">
                        <td class="py-3 px-4 font-mono text-slate-700">${h.date}</td>
                        <td class="py-3 px-4 font-medium">${h.correct_answers} / ${h.total_questions}</td>
                        <td class="py-3 px-4 font-bold ${h.functional_score >= 70 ? 'text-emerald-700' : 'text-rose-600'}">
                          ${h.functional_score.toFixed(1)} / 100
                        </td>
                        <td class="py-3 px-4 font-black text-slate-900">${h.total_weighted_score.toFixed(2)}</td>
                        <td class="py-3 px-4">
                          <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${
                            h.passed_functional ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
                          }">
                            ${h.passed_functional ? 'Aprobado' : 'Eliminado'}
                          </span>
                        </td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            `}
          </div>
        </div>
      `;
    } catch (err) {
      console.error(err);
    }
  },

  // -------------------------------------------------------------
  // 8. BIBLIOTECA NORMATIVA Y DOCUMENTOS OFICIALES
  // -------------------------------------------------------------
  async renderDocuments(container) {
    if (AppState.documents.items.length === 0) {
      try {
        AppState.documents.items = await API.getDocuments();
      } catch (err) {
        console.error('Error al cargar documentos:', err);
      }
    }

    const docs = AppState.documents.items;
    const currentCat = AppState.documents.selectedCategory;
    const filteredDocs = currentCat === 'all'
      ? docs
      : docs.filter(d => d.category === currentCat);

    const categories = ['all', 'Tributario', 'Procedimiento Administrativo', 'Transparencia', 'Gestión Documental', 'CNSC'];

    container.innerHTML = `
      <div class="space-y-6 animate-fade-in">
        <!-- Encabezado -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div class="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-xs font-bold mb-2">
              <span>📚 Fuentes Jurídicas Oficiales</span>
            </div>
            <h1 class="text-2xl md:text-3xl font-black text-slate-900">Biblioteca Normativa y Documentos Oficiales</h1>
            <p class="text-xs md:text-sm text-slate-500">
              Marco legal, leyes, decretos y guías oficiales requeridas para la OPEC 236799 (Ficha CC-AU-2010).
            </p>
          </div>
          <div class="text-xs font-medium text-slate-400 bg-white px-3 py-2 rounded-xl border border-slate-200">
            Total Recursos: <span class="font-bold text-slate-800">${docs.length}</span>
          </div>
        </div>

        <!-- Filtros por Categoría -->
        <div class="flex flex-wrap items-center gap-2">
          ${categories.map(cat => {
            const isSelected = currentCat === cat;
            const label = cat === 'all' ? 'Todos los Documentos' : cat;
            return `
              <button onclick="UI.filterDocumentsByCategory('${cat}')" class="px-3.5 py-1.5 rounded-xl text-xs font-bold transition ${
                isSelected
                  ? 'bg-emerald-700 text-white shadow-sm'
                  : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
              }">
                ${label}
              </button>
            `;
          }).join('')}
        </div>

        <!-- Grid de Recursos Normativos -->
        ${filteredDocs.length === 0 ? `
          <div class="p-8 bg-white rounded-2xl border border-slate-200 text-center text-slate-500 text-sm">
            No se encontraron documentos en esta categoría.
          </div>
        ` : `
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            ${filteredDocs.map(doc => {
              // Estilo de badge según categoría
              let badgeColor = 'bg-slate-100 text-slate-700 border-slate-200';
              if (doc.category === 'Tributario') badgeColor = 'bg-amber-100 text-amber-800 border-amber-200';
              if (doc.category === 'Procedimiento Administrativo') badgeColor = 'bg-emerald-100 text-emerald-800 border-emerald-200';
              if (doc.category === 'Transparencia') badgeColor = 'bg-sky-100 text-sky-800 border-sky-200';
              if (doc.category === 'Gestión Documental') badgeColor = 'bg-indigo-100 text-indigo-800 border-indigo-200';
              if (doc.category === 'CNSC') badgeColor = 'bg-rose-100 text-rose-800 border-rose-200';

              const isPdf = doc.file_type && doc.file_type.toLowerCase().includes('pdf');

              return `
                <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 hover:shadow-md transition flex flex-col justify-between group">
                  <div>
                    <!-- Badges -->
                    <div class="flex items-center justify-between gap-2 mb-3">
                      <span class="px-2.5 py-1 rounded-lg text-[11px] font-bold border ${badgeColor}">
                        ${doc.category}
                      </span>
                      <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${
                        isPdf ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-slate-100 text-slate-600 border border-slate-200'
                      }">
                        ${isPdf ? '📄 ' : '🌐 '}${doc.file_type}
                      </span>
                    </div>

                    <!-- Título -->
                    <h2 class="text-base font-bold text-slate-900 group-hover:text-emerald-800 transition mb-2 leading-snug">
                      ${doc.title}
                    </h2>

                    <!-- Descripción -->
                    <p class="text-xs text-slate-600 leading-relaxed mb-4">
                      ${doc.description}
                    </p>
                  </div>

                  <!-- Botón Enlace Externo Seguro -->
                  <div class="pt-4 border-t border-slate-100">
                    <a href="${doc.external_url}" target="_blank" rel="noopener noreferrer" class="w-full py-2.5 px-3 rounded-xl bg-slate-900 hover:bg-emerald-700 text-white text-xs font-bold transition flex items-center justify-center gap-2 shadow-sm">
                      <span>Ver / Consultar Online</span>
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                    </a>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        `}
      </div>
    `;
  },

  filterDocumentsByCategory(category) {
    AppState.documents.selectedCategory = category;
    this.render();
  }
};

// Arrancar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  UI.init();
});
