# PrepDIAN 2676 — Analista IV (OPEC 236799)
> Plataforma web de preparación, estudio y simulacros oficiales de juicio situacional para la Convocatoria DIAN 2676 (Asistencia al Usuario - Nivel Técnico).

---

## 🏛️ Datos Oficiales del Proceso
- **Proceso:** Selección DIAN 2676 - Ingreso (CNSC).
- **Cargo:** Analista IV | **Nivel:** Técnico | **Grado:** 4 | **Código:** 204.
- **OPEC:** 236799 | **Ficha Manual de Funciones:** CC-AU-2010 (Resolución 0067 de 2024).
- **Proceso / Subproceso:** Cercanía con el ciudadano / Asistencia al usuario.
- **Vacantes:** 3 plazas (Medellín, Tuluá y Arauca).

---

## ⚖️ Reglas Oficiales de Calificación
- **Prueba Funcional (65%):** Carácter **Eliminatorio**. Requiere un puntaje mínimo aprobatorio de **70.00 / 100** para no ser eliminado del proceso de selección.
- **Prueba Comportamental (15%):** Carácter Clasificatorio.
- **Prueba de Integridad (10%):** Carácter Clasificatorio.
- **Valoración de Antecedentes (10%):** Hoja de vida y experiencia acreditada.

---

## 🚀 Funcionalidades Principales
1. **Módulos de Estudio Teóricos (6 Módulos Oficiales):**
   - Módulo 1: Registro Único Tributario (RUT) — Estatuto Tributario Art. 555-2 y DUR 1625/2016.
   - Módulo 2: PQRSF, Derecho de Petición (Ley 1755/2015) y CPACA (Ley 1437/2011).
   - Módulo 3: Orientación Normativa TACI (Evasión vs. Elusión vs. Contrabando, IVA, Renta, RST).
   - Módulo 4: Canales de Atención DIAN, Instrumento de Firma Electrónica (IFE) y Atención Prioritaria.
   - Módulo 5: Transparencia (Ley 1712/2014, Reserva Art. 583 ET), Gestión Documental (Ley 594/2000) y MIPG.
   - Módulo 6: Competencias Comportamentales (Ficha CC-AU-2010) y Código de Integridad DIAN.
2. **Simulacro Real Cronometrado (Metodología Oficial CNSC):**
   - Casos laborales en seccionales DIAN con **3 opciones de respuesta (A, B y C)**.
   - Temporizador regresivo de 30 minutos.
   - Hoja de respuestas lateral interactiva y marcado de preguntas para revisión.
   - Calificación ponderada y dictamen oficial (Aprobado o Eliminado por umbral funcional).
   - Retroalimentación pedagógica detallada con citas normativas.
3. **Flashcards de Alto Rendimiento:**
   - Tarjetas interactivas con giro 3D para memorizar plazos legales perentorios y artículos clave.
4. **📚 Biblioteca Normativa y Documentos Oficiales:**
   - Enlaces oficiales a leyes, decretos, estatuto tributario y la guía del aspirante de la CNSC.
5. **Estadísticas e Historial:**
   - Registro de simulacros, promedios funcionales y evolución de desempeño.

---

## 🛠️ Stack Tecnológico
- **Backend:** Python 3.10+ / FastAPI, SQLAlchemy, SQLite, Pydantic v2.
- **Frontend:** HTML5 semántico, Tailwind CSS (CDN), Jinja2, JavaScript modular reactivo (SPA).

---

## 💻 Ejecución Local
```bash
# 1. Clonar el repositorio
git clone https://github.com/josealejot/simulacrodianpersonal.git
cd simulacrodianpersonal

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Iniciar servidor
python -m uvicorn main:app --reload --port 8000
```
Abre en tu navegador: `http://localhost:8000`.

---

## ☁️ Despliegue en la Nube (Render.com)
Para acceder desde tu celular 24/7 de forma gratuita:
1. Conecta este repositorio en [Render.com](https://render.com).
2. Crea un **New Web Service**.
3. Configuración:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. ¡Listo! Render te proporcionará una URL HTTPS pública (ej. `https://simulacrodian.onrender.com`).
