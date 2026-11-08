"""
Contenido ampliado PrepDIAN 2676 — organizado por los 14 ejes temáticos de la
ficha CC-AU-2010 (OPEC 236799 · Analista IV 204-4 · Asistencia al Usuario).

Fuente de los ejes: ficha del empleo en SIMO / Manual de Funciones (Res. 0067 de 2024).
Regla de la Guía de Orientación DIAN 2676: solo se evalúan normas vigentes expedidas
ANTES del 19 de junio de 2026.

Este módulo es ADITIVO: no modifica el contenido base de seed_service.py, solo lo
complementa. Cambiar CONTENT_VERSION fuerza la re-siembra del contenido de estudio
(el historial de simulacros nunca se borra).
"""
from sqlalchemy.orm import Session
from app.models.models import Module, Topic, Question, Option, Flashcard, DocumentResource

CONTENT_VERSION = "2026.11.07-ejes-opec-v2-links"

# =============================================================================
# EJES TEMÁTICOS OFICIALES (ficha CC-AU-2010) → módulos de estudio de la app
# =============================================================================
EJES_OPEC = [
    {
        "numero": 1, "grupo": "Propia del empleo",
        "titulo": "RUT: Registro Único Tributario",
        "modulos": [1],
        "claves": [
            "Art. 555-2 E.T.: el RUT es el mecanismo único para identificar, ubicar y clasificar a los sujetos de obligaciones administradas por la DIAN.",
            "Inscripción PREVIA al inicio de la actividad; actualización dentro del MES siguiente al hecho que la origina.",
            "Sanciones del Art. 658-3 E.T.: inscripción extemporánea / de oficio, desactualización e información falsa.",
            "Suspensión ≠ cancelación: la cancelación exige verificar que no haya obligaciones pendientes.",
            "Función esencial 4: veracidad y confiabilidad del RUT (validar identidad, dirección, prevenir suplantación).",
        ],
    },
    {
        "numero": 2, "grupo": "Propia del empleo",
        "titulo": "Dirección y administración de canales de servicio",
        "modulos": [4, 7],
        "claves": [
            "Canales: presencial, telefónico, virtual (portal, chat, videoatención) y escrito. Omnicanalidad.",
            "Indicadores: tiempo de espera, tiempo de atención, nivel de servicio, abandono, satisfacción, resolución en primer contacto.",
            "Gestión de demanda en picos (vencimientos de renta): agendamiento, reasignar capacidad, autogestión.",
            "Accesibilidad: atención preferente (Art. 5 num. 6 CPACA), ajustes razonables, Centro de Relevo.",
            "Instrumento de Firma Electrónica (IFE) y servicios informáticos electrónicos.",
        ],
    },
    {
        "numero": 3, "grupo": "Propia del empleo",
        "titulo": "Orientación normativa a los clientes TACI (tributario, aduanero, cambiario)",
        "modulos": [3],
        "claves": [
            "Obligación sustancial (pagar) vs. formales (RUT, declarar, facturar, informar).",
            "Renta personas naturales: topes de 1.400 UVT (ingresos, consumos, consignaciones) y 4.500 UVT (patrimonio).",
            "IVA: responsables vs. no responsables (3.500 UVT, Art. 437 par. 3); exento ≠ excluido.",
            "Régimen SIMPLE (Arts. 903-916 E.T.).",
            "Aduanero (Decreto 1165 de 2019) y cambiario (Ley 9 de 1991, DIAN controla operaciones de comercio exterior de bienes y servicios).",
        ],
    },
    {
        "numero": 4, "grupo": "Básica / común",
        "titulo": "Conceptos de Evasión, Elusión y Contrabando · Ley de Transparencia",
        "modulos": [3, 5],
        "claves": [
            "Evasión = ilegal (ocultar ingresos, costos ficticios). Elusión = abuso de formas jurídicas (Art. 869 E.T.).",
            "Contrabando abierto (por fuera del control aduanero) vs. técnico (con declaración, pero con fraude).",
            "Ley 1712 de 2014: máxima publicidad; información clasificada (Art. 18) vs. reservada (Art. 19); reserva máx. 15 años.",
            "Reserva tributaria (Art. 583 E.T.) prevalece frente a terceros, incluso periodistas.",
        ],
    },
    {
        "numero": 5, "grupo": "Básica / común",
        "titulo": "Herramientas Informáticas",
        "modulos": [8],
        "claves": [
            "Excel: referencias absolutas ($A$1), SUMA, PROMEDIO, CONTAR.SI, SUMAR.SI, SI, BUSCARV, filtros, tablas dinámicas.",
            "Word: combinar correspondencia, estilos y tabla de contenido, control de cambios.",
            "Correo: CCO para proteger direcciones de terceros.",
            "Seguridad digital: phishing, bloqueo de sesión, contraseñas, Ley 1273 de 2009, triada confidencialidad-integridad-disponibilidad.",
        ],
    },
    {
        "numero": 6, "grupo": "Básica / común",
        "titulo": "Gestión Documental",
        "modulos": [5],
        "claves": [
            "Ley 594 de 2000: ciclo vital (gestión → central → histórico).",
            "TRD (tiempos de retención) y TVD; transferencias primarias y secundarias; FUID.",
            "Principios de procedencia y orden original.",
            "Comunicaciones oficiales: radicación con consecutivo en ventanilla única (Acuerdo AGN 060 de 2001).",
            "Nunca eliminar documentos sin TRD/TVD aprobadas y aprobación del Comité.",
        ],
    },
    {
        "numero": 7, "grupo": "Básica / común",
        "titulo": "Modelo Integrado de Planeación y Gestión (MIPG)",
        "modulos": [5],
        "claves": [
            "Decreto 1499 de 2017: 7 dimensiones (Talento Humano es el corazón).",
            "Servicio al ciudadano, trámites, participación y gobierno digital → Dimensión 3 (Gestión con Valores para Resultados).",
            "Líneas de defensa: estratégica, 1.ª (líderes de proceso), 2.ª (planeación/riesgos), 3.ª (Control Interno).",
            "FURAG mide el desempeño institucional.",
        ],
    },
    {
        "numero": 8, "grupo": "Básica / común",
        "titulo": "Código de Buen Gobierno y Código de Integridad",
        "modulos": [9, 6],
        "claves": [
            "Ley 2016 de 2020: Código de Integridad obligatorio — Honestidad, Respeto, Compromiso, Diligencia, Justicia.",
            "Conflicto de intereses e impedimentos (Arts. 11-12 CPACA): declararse impedido en 3 días.",
            "Ley 1952 de 2019 (Código General Disciplinario) y delitos contra la administración pública (concusión, cohecho, prevaricato).",
            "Rechazar dádivas y denunciar.",
        ],
    },
    {
        "numero": 9, "grupo": "Básica / común",
        "titulo": "Principios de la Función Pública y Procedimiento Administrativo General (Ley 1437/2011 Tít. I, II y III caps. I, V-VIII)",
        "modulos": [10, 2],
        "claves": [
            "Art. 209 C.P. (7 principios) y Art. 3 CPACA (13 principios).",
            "Derechos de las personas (Art. 5), deberes de las autoridades (Art. 7: atención mínima 40 h/semana, carta de trato digno), prohibiciones (Art. 9).",
            "Notificaciones (personal, aviso, electrónica, conducta concluyente) y recursos (reposición, apelación: 10 días; queja: 5 días).",
            "Silencio negativo (3 meses; 2 meses en recursos), firmeza y pérdida de ejecutoriedad.",
            "OJO: actos tributarios tienen recurso propio — reconsideración en 2 meses (Art. 720 E.T.).",
        ],
    },
    {
        "numero": 10, "grupo": "Básica / común",
        "titulo": "Sistema PQRSF",
        "modulos": [2],
        "claves": [
            "Ley 1755 de 2015: 15 días (general), 10 (documentos), 30 (consultas), 5 (traslado por incompetencia).",
            "Petición incompleta: requerir en 10 días; 1 mes para completar; desistimiento tácito.",
            "Ampliación de término: avisar antes del vencimiento, hasta el doble del inicial.",
            "Diferenciar petición, queja, reclamo, sugerencia, felicitación y denuncia.",
        ],
    },
    {
        "numero": 11, "grupo": "Básica / común",
        "titulo": "Políticas Estatales de Servicio al Ciudadano",
        "modulos": [7],
        "claves": [
            "CONPES 3785 de 2013: ventanilla hacia adentro y ventanilla hacia afuera.",
            "Antitrámites (Ley 962/2005, Decreto Ley 019/2012): no exigir documentos que ya tiene la entidad.",
            "Ley 1474 de 2011 Art. 76: dependencia de quejas, sugerencias y reclamos.",
            "Atributos del buen servicio y lenguaje claro.",
        ],
    },
    {
        "numero": 12, "grupo": "Básica / común",
        "titulo": "Constitución Política: derechos fundamentales, principios y estructura del Estado",
        "modulos": [11],
        "claves": [
            "Art. 1 (Estado social de derecho), Art. 2 (fines), Art. 6 (responsabilidad de servidores).",
            "Derechos: petición (23), debido proceso (29), habeas data (15), igualdad (13); tutela (86).",
            "Ramas y órganos (Art. 113), órganos de control (Art. 117), carrera y mérito (Art. 125).",
            "Tributos: legalidad (Art. 338), equidad, eficiencia y progresividad (Art. 363), deber de contribuir (Art. 95-9).",
        ],
    },
    {
        "numero": 13, "grupo": "Básica / común",
        "titulo": "Función de asistencia al cliente",
        "modulos": [7, 4],
        "claves": [
            "Propósito y 7 funciones esenciales del empleo (ficha CC-AU-2010).",
            "Ciclo de atención: saludo → escucha → orientación con base normativa → verificación → cierre y registro.",
            "Asistir sin sustituir al contribuyente (no usar sus credenciales) y sin asesorar evasión.",
            "Manejo de usuarios difíciles y escalamiento.",
        ],
    },
    {
        "numero": 14, "grupo": "Básica / común",
        "titulo": "Cultura de la contribución",
        "modulos": [12],
        "claves": [
            "Deber constitucional de contribuir (Art. 95 num. 9) dentro de conceptos de justicia y equidad.",
            "Cumplimiento voluntario: educar, facilitar, persuadir y controlar.",
            "Programas pedagógicos (NAF, cultura de la contribución en la escuela) y su evaluación con indicadores.",
        ],
    },
    {
        "numero": 15, "grupo": "Pruebas Comportamental e Integridad",
        "titulo": "Competencias comportamentales e integridad (escala Likert)",
        "modulos": [6],
        "claves": [
            "Escala Likert de 4 opciones; la Guía DIAN 2676 incluye 2 subescalas de control de respuestas 'exageradamente favorables'.",
            "Responde con consistencia y realismo: no marques extremos por reflejo.",
            "Competencias: orientación al usuario, al logro, comportamiento ético, comunicación, trabajo en equipo, adaptabilidad.",
        ],
    },
]

# =============================================================================
# MÓDULOS NUEVOS (7 a 12)
# =============================================================================
NEW_MODULES = [
    {
        "number": 7,
        "title": "Servicio al Ciudadano y Función de Asistencia al Cliente",
        "subtitle": "CONPES 3785/2013, antitrámites, Ley 1474/2011 Art. 76, CPACA Arts. 5-9 y funciones de la ficha CC-AU-2010",
        "category": "Funcional", "priority": "Máxima", "icon": "users",
        "description": "Ejes 2, 11 y 13 de la OPEC: políticas estatales de servicio al ciudadano, protocolo de atención, manejo de usuarios difíciles y las 7 funciones esenciales del Analista IV en Asistencia al Usuario.",
        "topics": [
            ("Propósito y funciones esenciales del empleo (Ficha CC-AU-2010)", "Resolución 0067 de 2024 — Manual de Funciones DIAN",
             """### Propósito del empleo
Adelantar acciones técnicas y administrativas que faciliten la proyección, ejecución, evaluación y mejora de planes, programas y proyectos relacionados con el **Subproceso de Asistencia al Usuario**, de acuerdo con la normativa, políticas, procedimientos e instrucciones impartidas.

### Las 7 funciones esenciales (cada una es fuente de preguntas)
1. **Asistencia técnica** al cliente en temas tributarios, aduaneros o cambiarios, mediante los diferentes canales dispuestos por la Entidad.
2. **Control, direccionamiento y trámite de PQRSFD** (peticiones, quejas, sugerencias, reclamos, felicitaciones y denuncias) asignadas por el sistema.
3. **Tramitar inscripción o actualización en el RUT** y el control a obligaciones formales.
4. **Veracidad y confiabilidad de la información del RUT**: proponer y ejecutar estrategias (validación de identidad y dirección, cruces, prevención de suplantación).
5. **Asistir a los usuarios en campañas** propias del subproceso o institucionales (temporada de renta, actualización RUT, facturación electrónica, SIMPLE).
6. **Organización y evaluación de programas pedagógicos** que contribuyan a una mayor comprensión del sistema tributario (cultura de la contribución).
7. Las comunes a todos los empleos de la planta de la DIAN.

> **Clave para el examen:** las preguntas de juicio situacional describen a un Analista IV haciendo alguna de estas funciones. La respuesta correcta casi siempre: (1) aplica la norma, (2) protege los derechos del ciudadano, (3) respeta la reserva y la competencia, y (4) deja trazabilidad (radicar, registrar, informar)."""),
            ("Políticas estatales de servicio al ciudadano", "CONPES 3785 de 2013 · Decreto 1499 de 2017 · Ley 962 de 2005 · Decreto Ley 019 de 2012 · Ley 1474 de 2011",
             """### 1. Política Nacional de Eficiencia Administrativa al Servicio del Ciudadano (CONPES 3785 de 2013)
Modelo de dos ventanillas:
- **Ventanilla hacia adentro:** arreglos institucionales, procesos y procedimientos, talento humano, infraestructura, cobertura. Es lo que la entidad organiza internamente para servir bien.
- **Ventanilla hacia afuera:** canales de atención, certidumbre (información clara sobre tiempos, requisitos y costos) y cumplimiento de las expectativas del ciudadano.

### 2. Servicio al ciudadano dentro del MIPG
La política de **Servicio al Ciudadano** hace parte de la **Dimensión 3 — Gestión con Valores para Resultados** (relación Estado-ciudadano), junto con Racionalización de Trámites, Participación Ciudadana en la Gestión Pública y Gobierno Digital.

### 3. Antitrámites y racionalización
- **Ley 962 de 2005** y **Decreto Ley 019 de 2012**: simplificar trámites y eliminar requisitos innecesarios.
- **Prohibido exigir documentos que reposan en la entidad** (Decreto Ley 019 de 2012 Art. 9 y CPACA Art. 9). El servidor consulta sus propios sistemas.
- No se pueden exigir requisitos que no estén previstos en la ley.

### 4. Quejas, sugerencias y reclamos
- **Ley 1474 de 2011 Art. 76:** en toda entidad pública debe existir al menos una dependencia encargada de recibir, tramitar y resolver las quejas, sugerencias y reclamos de los ciudadanos.
- **Plan Anticorrupción y de Atención al Ciudadano** (Ley 1474 de 2011 Art. 73), que incluye un componente de mecanismos para mejorar la atención al ciudadano.

### 5. Atributos del buen servicio
Respetuoso · Amable · Confiable · Empático · Incluyente · Oportuno · Efectivo.
**Lenguaje claro:** frases cortas, sin tecnicismos innecesarios, verificando que el ciudadano entendió."""),
            ("Protocolo de atención y manejo de situaciones difíciles", "CPACA Arts. 5, 7 y 9 · Protocolos de Servicio al Ciudadano",
             """### 1. Ciclo de atención en 5 pasos
1. **Saludo e identificación**: presentarse, ofrecer ayuda, identificar al usuario cuando el trámite lo requiera.
2. **Escucha activa y diagnóstico**: entender qué necesita realmente (no lo que uno supone).
3. **Orientación o solución con base normativa**: explicar requisitos, plazos y canales; si no es competencia DIAN, indicar la entidad competente.
4. **Verificación de comprensión**: preguntar si quedó claro, resumir los pasos.
5. **Cierre y registro**: despedirse, registrar la atención o radicar la petición cuando aplique (trazabilidad).

### 2. Deberes de las autoridades en la atención al público (CPACA Art. 7)
- Dar trato respetuoso, considerado y diligente a todas las personas, sin distinción.
- Garantizar **atención personal al público como mínimo 40 horas a la semana**, en horarios que satisfagan las necesidades del servicio.
- Establecer un sistema de turnos acorde con las necesidades del servicio y las nuevas tecnologías.
- **Expedir y hacer visible la Carta de Trato Digno al usuario**, con sus derechos y los medios para garantizarlos.
- Tramitar las peticiones que lleguen por medios electrónicos.
- Atribuir a dependencias especializadas la atención de quejas y reclamos.

### 3. Prohibiciones (CPACA Art. 9) — muy preguntadas
- Negarse a recibir peticiones o a expedir constancias sobre ellas.
- **Exigir constancias, certificaciones o documentos que reposen en la propia entidad.**
- Demorar injustificadamente la producción de los actos o el trámite.
- Reproducir actos suspendidos o anulados.

### 4. Usuario alterado o agresivo
- Mantener la calma, no tomarlo como algo personal, escuchar sin interrumpir.
- Mostrar empatía ("entiendo su molestia") y enfocar la conversación en la solución.
- No prometer lo que no se puede cumplir.
- Si hay agresión verbal persistente o amenaza: advertir con respeto y, de ser necesario, **escalar al supervisor** o seguir el protocolo de seguridad.

### 5. Límites de la asistencia
- **Asistir no es sustituir:** el servidor orienta, pero las declaraciones las diligencia y firma el contribuyente con **su** IFE. Nunca usar credenciales del usuario ni las propias en su nombre.
- No asesorar conductas de evasión o elusión; sí informar los beneficios **legales** vigentes.
- Respetar la **reserva tributaria**: solo se informa al titular o a su apoderado debidamente identificado."""),
        ],
    },
    {
        "number": 8,
        "title": "Herramientas Informáticas y Seguridad Digital",
        "subtitle": "Ofimática (Excel, Word, correo), servicios informáticos electrónicos DIAN, Ley 1273/2009, Ley 527/1999",
        "category": "Funcional", "priority": "Media", "icon": "computer",
        "description": "Eje 5 de la OPEC: manejo de herramientas de oficina para el trabajo diario del Analista IV y buenas prácticas de seguridad de la información.",
        "topics": [
            ("Excel y Word para el trabajo diario", "Competencias ofimáticas básicas",
             """### 1. Excel — lo más preguntado
| Necesito… | Uso |
|---|---|
| Sumar un rango | `=SUMA(B2:B50)` |
| Promedio | `=PROMEDIO(B2:B50)` |
| Contar celdas con números / no vacías | `=CONTAR(...)` / `=CONTARA(...)` |
| Contar según un criterio | `=CONTAR.SI(C2:C500;"Queja")` |
| Sumar según un criterio | `=SUMAR.SI(C2:C500;"Medellín";D2:D500)` |
| Condición | `=SI(E2>15;"Vencida";"En término")` |
| Buscar un dato en otra tabla | `=BUSCARV(NIT;Tabla;columna;FALSO)` |
| Fecha de hoy | `=HOY()` |

- **Referencia relativa** (`A1`) cambia al copiar la fórmula; **referencia absoluta** (`$A$1`) queda fija. Mixtas: `$A1` (fija columna) o `A$1` (fija fila).
- **Filtros y ordenar**: para ver solo las PQRS de un tipo o vencidas.
- **Tabla dinámica**: resumir grandes volúmenes (ej. PQRS por tipo y por seccional) sin fórmulas.
- **Formato condicional**: resaltar automáticamente, por ejemplo, las peticiones a punto de vencer.
- **Validación de datos**: listas desplegables para evitar errores de digitación.

### 2. Word
- **Combinar correspondencia**: generar cartas personalizadas a partir de una lista en Excel.
- **Estilos de título + tabla de contenido** automática.
- **Control de cambios y comentarios**: revisar documentos en equipo dejando trazabilidad.

### 3. Correo electrónico institucional
- **Para**: destinatario principal · **CC**: copia visible · **CCO**: copia oculta. Para envíos masivos a ciudadanos se usa **CCO**, para no exponer las direcciones (datos personales).
- Asunto claro, lenguaje formal, no reenviar información reservada a cuentas personales."""),
            ("Seguridad digital y protección de la información", "Ley 1273 de 2009 · Ley 1581 de 2012 · Ley 527 de 1999 · Decreto 767 de 2022",
             """### 1. Principios de la seguridad de la información
- **Confidencialidad:** solo accede quien está autorizado.
- **Integridad:** la información no se altera sin autorización.
- **Disponibilidad:** está accesible cuando se necesita.

### 2. Amenazas frecuentes
- **Phishing** (correo falso), **smishing** (SMS), **vishing** (llamada): suplantan a la DIAN o a bancos para robar claves. La DIAN no solicita contraseñas por correo.
- **Ransomware**: secuestra la información y pide rescate.
- **Ingeniería social**: manipular a la persona para que entregue datos o accesos.

### 3. Buenas prácticas del servidor
- Bloquear la sesión al levantarse del puesto (tecla Windows + L).
- No compartir contraseñas; usar contraseñas robustas y doble factor de autenticación.
- No abrir enlaces ni adjuntos sospechosos; verificar por los canales oficiales.
- No conectar memorias USB desconocidas.
- **Reportar** cualquier incidente a la mesa de servicio o al área de seguridad de la información.

### 4. Marco legal
- **Ley 1273 de 2009 (delitos informáticos):** acceso abusivo a sistema informático (Art. 269A), violación de datos personales (Art. 269F), suplantación de sitios web para capturar datos personales (Art. 269G), hurto por medios informáticos (Art. 269I).
- **Ley 527 de 1999:** valor jurídico de los mensajes de datos y de la firma digital (equivalencia funcional).
- **Ley 1581 de 2012:** protección de datos personales.
- **Decreto 767 de 2022:** Política de Gobierno Digital (incluye seguridad y privacidad de la información)."""),
            ("Servicios informáticos electrónicos de la DIAN", "Resolución DIAN 000070 de 2016 (IFE) · Estatuto Tributario Art. 579-2",
             """### 1. Elementos básicos
- **Usuario registrado** en el portal DIAN: requisito para hacer trámites en línea.
- **Instrumento de Firma Electrónica (IFE):** permite firmar declaraciones y documentos en los servicios en línea. Es personal e intransferible.
- **Obligados a declarar virtualmente:** si presentan en papel, la declaración se tiene como no presentada.

### 2. Formularios que debes reconocer
| Formulario | Uso |
|---|---|
| 001 | RUT |
| 110 | Renta personas jurídicas (y naturales no residentes en ciertos casos) |
| 210 | Renta personas naturales residentes |
| 260 | Declaración anual consolidada Régimen SIMPLE |
| 300 | IVA |
| 350 | Retención en la fuente |

### 3. Factura electrónica
- Documento que **se valida previamente por la DIAN** antes de entregarse al adquirente.
- Si el adquirente no recibe facturas electrónicas, se le entrega la **representación gráfica** (física o digital). La representación gráfica no reemplaza la validación."""),
        ],
    },
    {
        "number": 9,
        "title": "Código de Buen Gobierno, Integridad y Régimen Disciplinario",
        "subtitle": "Ley 2016 de 2020, CPACA Arts. 11-12, Ley 1952 de 2019, Ley 1474 de 2011 y Código Penal",
        "category": "Funcional", "priority": "Alta", "icon": "scale",
        "description": "Eje 8 de la OPEC: valores del servicio público, conflicto de intereses, impedimentos, faltas disciplinarias y delitos contra la administración pública.",
        "topics": [
            ("Código de Integridad del Servicio Público", "Ley 2016 de 2020 · Decreto 1499 de 2017 (política de integridad MIPG)",
             """### Los 5 valores (adoptados con carácter obligatorio por la Ley 2016 de 2020)
| Valor | Lo que hago | Lo que no hago |
|---|---|---|
| **Honestidad** | Actúo con fundamento en la verdad, con transparencia y rectitud, favoreciendo el interés general. | No acepto dádivas ni uso el cargo para beneficio propio; no oculto errores. |
| **Respeto** | Trato con dignidad a todas las personas, sin importar su condición. | No discrimino, no humillo, no grito. |
| **Compromiso** | Comprendo la importancia de mi rol y busco resolver las necesidades de las personas. | No trabajo con apatía ni pienso que mi labor es "solo un trabajo". |
| **Diligencia** | Cumplo mis deberes con atención, prontitud, destreza y eficiencia, cuidando los recursos públicos. | No dejo trámites represados ni malgasto recursos. |
| **Justicia** | Actúo con imparcialidad, equidad e igualdad. | No favorezco a nadie por amistad, política o interés. |

> **Tip de examen:** si el caso describe "prontitud, oportunidad, buen uso de recursos" → Diligencia. Si describe "imparcialidad, sin favoritismos" → Justicia. Si describe "verdad, no aceptar beneficios" → Honestidad."""),
            ("Buen Gobierno: conflicto de intereses e impedimentos", "CPACA Arts. 11 y 12 · Ley 1952 de 2019 · Ley 2013 de 2019",
             """### 1. ¿Qué es un conflicto de intereses?
Situación en la que el interés particular del servidor (o de sus familiares o socios) puede interferir con el interés general que debe proteger al decidir o actuar.

### 2. Causales de impedimento y recusación (CPACA Art. 11) — las más preguntadas
- Tener interés particular y directo en la decisión el servidor, su cónyuge o compañero(a) permanente, o sus parientes **hasta el cuarto grado de consanguinidad, segundo de afinidad o primero civil**, o su socio(s) de hecho o de derecho.
- Haber conocido del asunto en oportunidad anterior, haber sido apoderado o haber dado consejo sobre él.
- Existir enemistad grave o amistad entrañable con alguno de los interesados.
- Existir litigio o controversia ante autoridades entre el servidor y los interesados.

*Grados de consanguinidad:* padres e hijos (1.º), hermanos, abuelos y nietos (2.º), tíos y sobrinos (3.º), **primos (4.º)**.

### 3. Trámite del impedimento (CPACA Art. 12)
El servidor, **dentro de los 3 días siguientes** a conocer la causal, envía la actuación con escrito motivado a su **superior**, quien decide de plano **dentro de los 10 días siguientes** y, si lo acepta, designa quién debe conocer del asunto.

### 4. Código de Buen Gobierno
Documento que recoge los compromisos éticos de la dirección frente a los grupos de interés: transparencia, rendición de cuentas, manejo de conflictos de intereses, relación con órganos de control, lucha contra la corrupción y contratación transparente.
**Ley 2013 de 2019:** publicación de la declaración de bienes y rentas, del registro de conflictos de interés y de la declaración del impuesto sobre la renta de los servidores obligados."""),
            ("Régimen disciplinario y delitos contra la administración pública", "Ley 1952 de 2019 (modificada por Ley 2094 de 2021) · Ley 599 de 2000 · Ley 1474 de 2011 · Ley 906 de 2004 Art. 67",
             """### 1. Código General Disciplinario (Ley 1952 de 2019)
Faltas: **gravísimas, graves y leves**. Sanciones según la falta y la culpabilidad:
| Falta | Sanción |
|---|---|
| Gravísima con dolo o culpa gravísima | **Destitución e inhabilidad general** |
| Grave dolosa | Suspensión en el ejercicio del cargo e inhabilidad especial |
| Grave culposa | Suspensión |
| Leve dolosa | Multa |
| Leve culposa | Amonestación escrita |

### 2. Delitos contra la administración pública (Código Penal)
- **Peculado:** apropiarse o usar indebidamente bienes del Estado que administra en razón de sus funciones.
- **Concusión (Art. 404):** el servidor, abusando del cargo, **constriñe o induce** a alguien a dar o prometer dinero o utilidad indebidos.
- **Cohecho propio (Art. 405):** recibir dinero o utilidad para **retardar u omitir** un acto propio del cargo o ejecutar uno **contrario** a sus deberes.
- **Cohecho impropio (Art. 406):** aceptar dinero o utilidad para ejecutar un acto **propio** de sus funciones.
- **Cohecho por dar u ofrecer (Art. 407):** lo comete el particular que ofrece.
- **Prevaricato** por acción (Art. 413: decisión manifiestamente contraria a la ley) y por omisión (Art. 414).
- **Tráfico de influencias** (Art. 411), **revelación de secreto** (Art. 418), **utilización indebida de información privilegiada** (Art. 420).

### 3. Deber de denunciar
El servidor público que conozca de un delito debe **denunciarlo** ante la autoridad competente (Ley 906 de 2004 Art. 67); también debe poner en conocimiento las faltas disciplinarias.
**Ley 1474 de 2011 (Estatuto Anticorrupción):** medidas administrativas, penales y disciplinarias contra la corrupción."""),
        ],
    },
    {
        "number": 10,
        "title": "Principios de la Función Pública y Procedimiento Administrativo (CPACA)",
        "subtitle": "Constitución Art. 209 · Ley 1437 de 2011: Título I, Título III caps. I, V, VI, VII y VIII",
        "category": "Funcional", "priority": "Máxima", "icon": "building-library",
        "description": "Eje 9 de la OPEC, que la ficha delimita expresamente: disposiciones generales, principios, reglas generales del procedimiento, notificaciones, recursos, silencio administrativo y conclusión del procedimiento.",
        "topics": [
            ("Título I CPACA: principios, derechos y deberes", "Constitución Art. 209 · Ley 1437 de 2011 Arts. 1 a 12",
             """### 1. Principios de la función administrativa (C.P. Art. 209) — 7
**Igualdad, moralidad, eficacia, economía, celeridad, imparcialidad y publicidad**, mediante descentralización, delegación y desconcentración de funciones.

### 2. Principios del CPACA (Art. 3) — 13
Debido proceso · Igualdad · Imparcialidad · Buena fe · Moralidad · Participación · Responsabilidad · Transparencia · Publicidad · Coordinación · **Eficacia** · Economía · Celeridad.
- **Eficacia:** las autoridades buscarán que los procedimientos logren su finalidad, **removerán de oficio los obstáculos puramente formales**, evitarán decisiones inhibitorias y sanearán irregularidades.
- **Economía:** proceder con austeridad y eficiencia, optimizando el uso del tiempo y de los recursos.
- **Celeridad:** impulsar oficiosamente los procedimientos, sin dilaciones injustificadas.
- **Buena fe:** se presume en todas las actuaciones de los particulares (también C.P. Art. 83).

### 3. Formas de iniciar las actuaciones (Art. 4)
Por quienes ejerciten el derecho de petición (interés general o particular), por quienes obren en cumplimiento de una obligación o deber legal, o **de oficio** por las autoridades.

### 4. Derechos de las personas ante las autoridades (Art. 5) — destacados
- Presentar peticiones en cualquier modalidad (verbal, escrita o por cualquier medio idóneo) **sin necesidad de apoderado**.
- Conocer el estado de sus trámites y obtener copias a su costa.
- Recibir trato digno.
- **Atención especial y preferente** a personas en situación de discapacidad, niños, niñas, adolescentes, mujeres gestantes, adultos mayores y, en general, personas en estado de indefensión o debilidad manifiesta (num. 6).

### 5. Deberes de las personas (Art. 6)
Acatar la Constitución y las leyes, obrar con lealtad y buena fe, no hacer afirmaciones temerarias ni aportar documentos falsos, tratar respetuosamente a los servidores.

### 6. Deberes de las autoridades (Art. 7), deber de información (Art. 8) y prohibiciones (Art. 9)
Ver el módulo 7 (atención mínima de **40 horas semanales**, **Carta de Trato Digno**, no exigir documentos que reposan en la entidad).
**Art. 10 — Aplicación uniforme:** aplicar las normas y la jurisprudencia de manera uniforme a situaciones con los mismos supuestos fácticos y jurídicos."""),
            ("Título III cap. I: reglas generales del procedimiento", "Ley 1437 de 2011 Arts. 34 a 45",
             """### Reglas que más se preguntan
- **Art. 34 — Procedimiento común y supletivo:** las actuaciones se sujetan al procedimiento del CPACA **sin perjuicio de los procedimientos regulados en leyes especiales**; en lo no previsto en ellas se aplica el CPACA. → Por eso el **procedimiento tributario del E.T.** prevalece en asuntos de impuestos.
- **Art. 35:** las actuaciones pueden iniciarse por escrito, verbalmente o por medios electrónicos.
- **Art. 36:** un solo expediente por asunto; cualquier persona tiene derecho a examinarlo salvo reserva.
- **Arts. 37 y 38:** comunicar la actuación a terceros que puedan resultar afectados; estos pueden intervenir.
- **Art. 40 — Pruebas:** pueden aportarse, pedirse y practicarse hasta antes de la decisión de fondo; son admisibles los medios de prueba del Código General del Proceso.
- **Art. 42 — Contenido de la decisión:** acto **motivado** que resuelve **todas** las peticiones planteadas.
- **Art. 43 — Actos definitivos:** deciden directa o indirectamente el fondo del asunto o hacen imposible continuar la actuación.
- **Art. 44 — Decisiones discrecionales:** deben ser adecuadas a los fines de la norma y proporcionales a los hechos.
- **Art. 45 — Corrección de errores formales:** errores aritméticos, de digitación, de transcripción o de omisión de palabras pueden corregirse **en cualquier tiempo, de oficio o a petición de parte**; **no revive los términos** para recursos."""),
            ("Notificaciones, recursos, silencio y conclusión del procedimiento", "Ley 1437 de 2011 Arts. 65 a 97 · Estatuto Tributario Art. 720",
             """### 1. Publicidad y notificación (Cap. V, Arts. 65-73)
- **Actos generales:** se **publican** (Diario Oficial o gacetas) — Art. 65.
- **Actos particulares:** se **notifican** — Art. 66.
- **Personal (Art. 67):** se entrega copia íntegra, auténtica y gratuita del acto, indicando recursos, autoridad ante quien se interponen y plazos.
- **Citación (Art. 68):** si no hay otro medio más eficaz, se envía citación para que comparezca **dentro de los 5 días** siguientes.
- **Aviso (Art. 69):** si no se pudo notificar personalmente al cabo de esos 5 días, se envía aviso con copia del acto; la notificación queda surtida **al finalizar el día siguiente** a la entrega del aviso. Si se desconoce la dirección, el aviso se publica en la página web y en lugar de acceso al público por **5 días**.
- **Electrónica (Art. 56):** cuando el interesado la acepta (y en los casos que la ley lo prevé).
- **Conducta concluyente (Art. 72):** sin notificación en debida forma el acto no produce efectos, **salvo** que el interesado revele que lo conoce, consienta la decisión o **interponga los recursos**.

### 2. Recursos (Cap. VI, Arts. 74-82)
| Recurso | Ante quién | Plazo |
|---|---|---|
| **Reposición** | Mismo funcionario que decidió | 10 días siguientes a la notificación |
| **Apelación** | Superior inmediato administrativo o funcional | 10 días (directa o subsidiaria a la reposición) |
| **Queja** | Superior del que rechazó la apelación | 5 días siguientes a la notificación del rechazo |

- **Art. 75 — Improcedencia:** no hay recurso contra actos de **carácter general**, ni contra actos de **trámite, preparatorios o de ejecución** (salvo norma expresa).
- **Art. 76:** reposición y queja **no son obligatorias** (no son requisito para demandar); la apelación sí se exige para acudir a la jurisdicción cuando procede.
- **Art. 77 — Requisitos:** dentro del plazo, por el interesado o su apoderado, **sustentado con los motivos de inconformidad**, con las pruebas que se pretenda hacer valer y los datos del recurrente.
- **Art. 79:** se tramitan en efecto suspensivo; término para pruebas no mayor de **30 días**.

> **Diferencia clave en la DIAN:** contra las **liquidaciones oficiales y resoluciones que imponen sanciones tributarias** procede el **recurso de reconsideración**, dentro de los **2 meses** siguientes a la notificación (**Art. 720 E.T.**). El CPACA aplica de forma supletiva (Art. 34).

### 3. Silencio administrativo (Cap. VII, Arts. 83-86)
- **Negativo (Art. 83):** **3 meses** sin notificar decisión sobre una petición → se entiende negada. No exime a la autoridad del deber de decidir (salvo que el interesado ya haya recurrido el acto presunto o demandado y se haya notificado el auto admisorio).
- **Positivo (Art. 84):** solo en los casos **expresamente previstos** en la ley (ej. petición de documentos, Ley 1755 Art. 14).
- **Protocolización (Art. 85):** quien invoque el silencio positivo protocoliza la constancia de la petición con declaración jurada de no haber sido notificado.
- **En recursos (Art. 86):** **2 meses** sin decidir reposición o apelación → decisión negativa.

### 4. Conclusión del procedimiento (Cap. VIII, Arts. 87-92)
- **Firmeza (Art. 87):** cuando no proceden recursos (desde el día siguiente a la notificación), cuando se deciden los recursos, cuando vence el término sin interponerlos o se renuncia a ellos, cuando se acepta el desistimiento, o con la protocolización del silencio positivo.
- **Presunción de legalidad (Art. 88):** los actos se presumen legales mientras no sean anulados por la jurisdicción.
- **Carácter ejecutorio (Art. 89):** los actos en firme son suficientes para que la administración los ejecute.
- **Pérdida de ejecutoriedad (Art. 91):** (1) suspensión provisional; (2) desaparición de sus fundamentos de hecho o de derecho; (3) **cuando al cabo de 5 años de estar en firme la autoridad no ha realizado los actos para ejecutarlos**; (4) cumplimiento de la condición resolutoria; (5) pérdida de vigencia.

### 5. Dato extra: revocatoria directa (Arts. 93-97)
Causales: manifiesta oposición a la Constitución o a la ley; no conformidad con el interés público o social; agravio injustificado a una persona. Para revocar un acto particular y concreto se requiere el **consentimiento previo, expreso y escrito** del titular (Art. 97)."""),
        ],
    },
    {
        "number": 11,
        "title": "Constitución Política: Derechos, Principios y Estructura del Estado",
        "subtitle": "Arts. 1-10, 11-41, 83-95, 113-131, 209, 338 y 363 de la Constitución de 1991",
        "category": "Funcional", "priority": "Alta", "icon": "flag",
        "description": "Eje 12 de la OPEC: principios fundamentales, derechos fundamentales y sus mecanismos de protección, estructura del Estado y principios del sistema tributario.",
        "topics": [
            ("Principios fundamentales y deberes", "Constitución Política Arts. 1-10, 83, 95, 122-125",
             """### Artículos imprescindibles
- **Art. 1:** Colombia es un **Estado social de derecho**, organizado en forma de **república unitaria, descentralizada**, con autonomía de sus entidades territoriales, **democrática, participativa y pluralista**, fundada en el respeto de la dignidad humana, el trabajo, la solidaridad y la prevalencia del interés general.
- **Art. 2 — Fines esenciales:** servir a la comunidad, promover la prosperidad general y garantizar la efectividad de los principios, derechos y deberes; facilitar la participación. Las autoridades están instituidas para proteger a todas las personas.
- **Art. 4:** la Constitución es **norma de normas** (supremacía constitucional).
- **Art. 6:** los particulares responden por infringir la Constitución y las leyes; **los servidores públicos por lo mismo y por omisión o extralimitación en el ejercicio de sus funciones**.
- **Art. 83:** las actuaciones de particulares y autoridades deben ceñirse a la **buena fe**, que se presume.
- **Art. 95 num. 9:** es deber de la persona y del ciudadano **contribuir al financiamiento de los gastos e inversiones del Estado dentro de conceptos de justicia y equidad**.
- **Art. 122:** no habrá empleo público que no tenga funciones detalladas en ley o reglamento.
- **Art. 123:** son servidores públicos los miembros de las corporaciones públicas, los empleados y trabajadores del Estado y de sus entidades descentralizadas.
- **Art. 125:** los empleos del Estado son **de carrera** (salvo excepciones); el ingreso y el ascenso se hacen por **méritos** mediante concurso.
- **Art. 130:** la **Comisión Nacional del Servicio Civil (CNSC)** administra y vigila las carreras de los servidores públicos.
- **Art. 209:** principios de la función administrativa (igualdad, moralidad, eficacia, economía, celeridad, imparcialidad y publicidad)."""),
            ("Derechos fundamentales y mecanismos de protección", "Constitución Política Arts. 11-41, 74, 85-88 · Decreto 2591 de 1991",
             """### 1. Derechos fundamentales más relacionados con el cargo
- **Art. 13 — Igualdad** y protección especial a personas en debilidad manifiesta.
- **Art. 15 — Intimidad y habeas data:** derecho a conocer, **actualizar y rectificar** la información recogida sobre las personas en bancos de datos.
- **Art. 20 — Libertad de expresión e información.**
- **Art. 23 — Derecho de petición:** presentar peticiones respetuosas por motivos de interés general o particular y obtener **pronta resolución**.
- **Art. 29 — Debido proceso:** aplica a toda clase de actuaciones judiciales y administrativas.
- **Art. 74 — Acceso a documentos públicos**, salvo los casos que establezca la ley.
- **Art. 85:** derechos de **aplicación inmediata**.

### 2. Mecanismos de protección
| Mecanismo | Protege | Dato clave |
|---|---|---|
| **Acción de tutela (Art. 86)** | Derechos fundamentales | Protección inmediata; el juez decide en **máximo 10 días**; es **subsidiaria** (salvo perjuicio irremediable). Reglamentada por el Decreto 2591 de 1991. |
| **Habeas corpus (Art. 30)** | Libertad personal | Se resuelve en 36 horas. |
| **Acción de cumplimiento (Art. 87)** | Cumplimiento de una ley o acto administrativo | Ley 393 de 1997. |
| **Acciones populares y de grupo (Art. 88)** | Derechos colectivos / perjuicio a un grupo | Ley 472 de 1998. |

> Si la DIAN no responde una petición, el ciudadano puede acudir a la **tutela** por vulneración del derecho fundamental de petición."""),
            ("Estructura del Estado y principios tributarios", "Constitución Política Arts. 113-120, 150-12, 189, 267, 338, 363, 371",
             """### 1. Ramas del poder público (Art. 113)
Ramas **legislativa, ejecutiva y judicial**, más **órganos autónomos e independientes**. Los distintos órganos tienen funciones separadas pero colaboran armónicamente.
- **Legislativa:** Congreso (Senado y Cámara). Hace las leyes y ejerce control político. Establece las contribuciones fiscales (Art. 150 num. 12).
- **Ejecutiva:** el Presidente es **Jefe de Estado, Jefe de Gobierno y Suprema Autoridad Administrativa** (Art. 115); ministerios, departamentos administrativos, superintendencias, unidades administrativas especiales, gobernaciones y alcaldías.
- **Judicial (Art. 116):** Corte Constitucional, Corte Suprema de Justicia, Consejo de Estado, Comisión Nacional de Disciplina Judicial, Fiscalía General, tribunales y jueces.

### 2. Órganos de control (Art. 117) y organización electoral (Art. 120)
- **Ministerio Público:** Procuraduría General (control **disciplinario**), Defensoría del Pueblo y personerías.
- **Contraloría General de la República:** control **fiscal** (Art. 267).
- **Organización electoral:** Consejo Nacional Electoral y Registraduría Nacional del Estado Civil.
- **Banco de la República (Art. 371):** autoridad **monetaria, cambiaria y crediticia**.

### 3. La DIAN en la estructura del Estado
Unidad Administrativa Especial del orden nacional, **adscrita al Ministerio de Hacienda y Crédito Público** (rama ejecutiva). Su carrera es un **sistema específico de carrera** (Decreto Ley 071 de 2020), cuyos concursos realiza la CNSC.

### 4. Principios del sistema tributario
- **Art. 338 — Legalidad:** en tiempo de paz, **solamente el Congreso, las asambleas departamentales y los concejos** pueden imponer contribuciones; la ley, ordenanza o acuerdo debe fijar sujetos activos y pasivos, hechos y bases gravables y tarifas.
- **Art. 363:** el sistema tributario se funda en los principios de **equidad, eficiencia y progresividad**. Las leyes tributarias **no se aplican con retroactividad**.
- **Art. 189 num. 20:** al Presidente le corresponde velar por la estricta recaudación y administración de las rentas públicas.
- **Art. 95 num. 9:** deber de contribuir."""),
        ],
    },
    {
        "number": 12,
        "title": "Cultura de la Contribución y Programas Pedagógicos",
        "subtitle": "Constitución Art. 95-9, cumplimiento voluntario, NAF y evaluación de programas (función esencial 6)",
        "category": "Funcional", "priority": "Media", "icon": "academic-cap",
        "description": "Eje 14 de la OPEC y función esencial 6: promover la comprensión del sistema tributario y el cumplimiento voluntario mediante programas pedagógicos medibles.",
        "topics": [
            ("Fundamentos de la cultura de la contribución", "Constitución Política Arts. 95 num. 9, 338 y 363",
             """### 1. Concepto
Conjunto de **valores, actitudes y comportamientos** de la ciudadanía frente a los tributos, que favorecen el **cumplimiento voluntario** de las obligaciones tributarias, aduaneras y cambiarias, entendiendo que los impuestos financian bienes y servicios colectivos (salud, educación, infraestructura, seguridad).

### 2. Ideas fuerza para orientar al ciudadano
- Contribuir es un **deber constitucional** (Art. 95 num. 9) dentro de conceptos de justicia y equidad.
- El impuesto **no es una contraprestación individual**: se paga aunque el ciudadano no reciba un servicio directo y particular.
- La evasión y el contrabando trasladan la carga a quienes sí cumplen y afectan la competencia leal.
- La transparencia en el uso de los recursos públicos fortalece la confianza y la disposición a contribuir.

### 3. Modelo de cumplimiento
Las administraciones tributarias combinan cuatro estrategias según el comportamiento del contribuyente:
1. **Educar** a quien no conoce sus obligaciones.
2. **Facilitar** a quien quiere cumplir (servicios, simplificación, canales virtuales).
3. **Persuadir** a quien duda (comunicaciones, percepción de riesgo).
4. **Controlar** a quien decide no cumplir (fiscalización y sanción).
El Analista IV en Asistencia al Usuario trabaja sobre todo en **educar y facilitar**."""),
            ("Diseño y evaluación de programas pedagógicos", "Función esencial 6 — Ficha CC-AU-2010 · ciclo PHVA",
             """### 1. Programas pedagógicos de referencia en la DIAN
- **NAF — Núcleos de Apoyo Contable y Fiscal:** convenios entre la DIAN y universidades; estudiantes formados y supervisados brindan **orientación gratuita** a personas naturales, emprendedores y pequeñas empresas sobre RUT, factura electrónica, declaración de renta, etc.
- **Cultura de la contribución en la escuela:** formación a docentes y estudiantes sobre el sentido de lo público y de los tributos.
- Charlas, ferias de servicio, talleres de temporada de renta y contenidos digitales.

### 2. Ciclo de un programa (PHVA)
1. **Planear:** diagnóstico de necesidades y público objetivo; objetivos de aprendizaje medibles; metodología y recursos.
2. **Hacer:** ejecutar talleres o campañas, registrar asistencia y evidencias.
3. **Verificar:** evaluar con **indicadores**.
4. **Actuar:** ajustar el programa con base en los resultados.

### 3. Indicadores para evaluar
| Tipo | Ejemplo |
|---|---|
| Cobertura | Número de personas formadas frente a la meta |
| Aprendizaje | Diferencia entre prueba de entrada y de salida |
| Satisfacción | Encuesta al finalizar |
| Resultado / impacto | Aumento de declaraciones oportunas o de inscripciones correctas en el RUT en la población atendida |
| Eficiencia | Costo por persona formada |

> Evaluar no es contar folletos entregados: hay que medir si el público **aprendió** y si **cambió su comportamiento de cumplimiento**."""),
        ],
    },
]

# =============================================================================
# TEMAS ADICIONALES PARA LOS MÓDULOS BASE (1 a 6)
# =============================================================================
EXTRA_TOPICS = {
    1: [
        ("Generalidades del RUT y sanciones (Arts. 555-2 y 658-3 E.T.)", "Estatuto Tributario Arts. 555-2 y 658-3 · DUR 1625 de 2016",
         """### 1. Qué es el RUT
- **Art. 555-2 E.T.:** el Registro Único Tributario es el **mecanismo único para identificar, ubicar y clasificar** a los sujetos de obligaciones administradas y controladas por la DIAN.
- El **NIT** (Número de Identificación Tributaria) es el número que identifica al inscrito.
- Se diligencia en el **formulario 001**.
- La inscripción debe hacerse **antes de iniciar** la actividad económica que genera la obligación. Para comerciantes, la inscripción puede tramitarse a través de la **Cámara de Comercio** junto con el registro mercantil.
- Canales: presencial (con cita) y virtual (usuario registrado + IFE).

### 2. Sanciones relativas al RUT (Art. 658-3 E.T.) — concepto general
- **Inscripción extemporánea o de oficio:** multa por **cada día de retraso**, expresada en UVT.
- **No actualizar la información** dentro del mes siguiente al hecho: multa por **cada día de retraso**, expresada en UVT.
- **Suministrar información falsa** o hacerse inscribir con documentos falsos o suplantando a otro: sanción pecuniaria (además de las consecuencias penales).
> En el examen basta con identificar **qué conducta** es sancionable y que la base es el Art. 658-3 E.T.; no memorices cifras que puedan haber cambiado.

### 3. Recuerda
- Suspender **no extingue** la inscripción: la inhabilita temporalmente.
- Cancelar **sí** la extingue, y exige verificar que no haya obligaciones pendientes."""),
        ("Veracidad y confiabilidad de la información del RUT (función esencial 4)", "Ficha CC-AU-2010 · DUR 1625 de 2016 · Ley 1273 de 2009",
         """### Riesgos que afectan la calidad del RUT
- **Suplantación de identidad** para crear personas o empresas fachada (facturación falsa, devoluciones indebidas).
- **Direcciones inexistentes** o desactualizadas (contribuyente no ubicable).
- Actividades económicas (CIIU) o responsabilidades mal clasificadas.

### Estrategias que puede proponer y ejecutar el Analista IV
1. **Validación de identidad** rigurosa (documento original, cotejo de datos y biometría cuando esté disponible).
2. **Verificación de la dirección** y de los datos de contacto.
3. **Cruces de información** con terceros (Registraduría, Cámaras de Comercio, entidades financieras).
4. **Campañas de actualización** del RUT dirigidas a grupos con datos desactualizados.
5. **Reporte inmediato** de inconsistencias o indicios de fraude por los canales internos.

### Ante sospecha de suplantación
**No formalizar** el trámite, aplicar el protocolo interno de validación y reportar según el procedimiento, **sin** acusar públicamente ni retener arbitrariamente a la persona."""),
    ],
    2: [
        ("Reglas complementarias del derecho de petición (Ley 1755 de 2015)", "Ley 1755 de 2015 Arts. 13 a 26 · Ley 4 de 1913 Art. 62",
         """### 1. Reglas generales
- **Art. 13:** toda actuación que inicie cualquier persona ante las autoridades implica el ejercicio del derecho de petición. Es **gratuito** y **no requiere abogado**.
- **Art. 15:** puede presentarse **verbalmente, por escrito o por cualquier medio idóneo** (incluidos los electrónicos).
- **Art. 16 — Contenido mínimo:** autoridad a la que se dirige; nombres, apellidos, identificación y dirección del solicitante; objeto; razones; relación de documentos; firma cuando sea el caso.
- **Cómputo:** los plazos en **días** son **hábiles** (Ley 4 de 1913 Art. 62); los de meses y años, calendario.

### 2. Términos especiales
- **Art. 14 parágrafo — Ampliación:** si no es posible responder en el plazo, se informa al interesado **antes del vencimiento**, con los motivos y el plazo razonable, que **no puede exceder del doble** del inicialmente previsto.
- **Art. 17 — Incompleta:** la autoridad requiere al peticionario **dentro de los 10 días** siguientes a la radicación para que complete en **1 mes** (prorrogable hasta por un término igual a solicitud). Si no completa → **desistimiento tácito** (acto motivado, con recurso de reposición).
- **Art. 18:** desistimiento expreso en cualquier tiempo.
- **Art. 19 — Irrespetuosas, oscuras o reiterativas:** las irrespetuosas se rechazan; si no se comprende la finalidad, se devuelve para que se corrija o aclare **dentro de los 10 días** siguientes; frente a las reiterativas ya resueltas, la autoridad puede **remitirse a las respuestas anteriores** (salvo derechos imprescriptibles o peticiones no resueltas de fondo).
- **Art. 20 — Atención prioritaria:** peticiones de reconocimiento de un derecho fundamental para evitar un perjuicio irremediable; y las de **periodistas** para el ejercicio de su actividad se tramitan **preferencialmente**.
- **Art. 21 — Incompetencia:** si se presentó **verbalmente**, se informa en el mismo acto; si fue por escrito, se remite a la autoridad competente **dentro de los 5 días** con copia al peticionario.

### 3. Información reservada
- **Art. 24:** enumera las informaciones y documentos con reserva (entre ellos los protegidos por reserva legal, como la tributaria).
- **Art. 25:** el rechazo por reserva debe ser **motivado**, indicando las disposiciones legales.
- **Art. 26 — Insistencia:** si el peticionario insiste, el asunto se envía al **juez o tribunal administrativo**, que decide en **10 días**."""),
        ("Gestión de PQRSFD en la DIAN: calidad de la respuesta", "Ley 1755 de 2015 · Ley 1474 de 2011 Art. 76 · Jurisprudencia de la Corte Constitucional",
         """### 1. Requisitos de una respuesta válida (jurisprudencia constitucional)
La respuesta debe ser **de fondo, clara, precisa, congruente con lo solicitado y oportuna**, y debe **ponerse en conocimiento** del peticionario. Responder no significa acceder: puede ser negativa, pero motivada.

### 2. Ruta interna según el tipo
| Tipo | Tratamiento |
|---|---|
| Petición | Resolver dentro de los términos de la Ley 1755 |
| Queja contra un servidor | Trámite y remisión a **Control Disciplinario Interno** |
| Reclamo por el servicio | Área responsable del servicio; acciones de mejora |
| Sugerencia | Análisis para mejora del proceso |
| Felicitación | Comunicar al servidor o área y registrar |
| Denuncia (contrabando, evasión, corrupción) | Área competente (fiscalización, control, anticorrupción) |

### 3. Buenas prácticas del Analista IV
- Clasificar bien desde el inicio (una mala clasificación cambia el plazo y la ruta).
- Controlar los términos con alertas (Excel o sistema).
- Dejar trazabilidad: radicado, fecha, responsable y respuesta."""),
    ],
    3: [
        ("Renta e IVA: lo que más consultan los usuarios", "Estatuto Tributario Arts. 10, 420, 437 par. 3, 592-594-3 · Ley 2277 de 2022",
         """### 1. ¿Quién declara renta? (personas naturales residentes)
Debe declarar quien en el año gravable supere **cualquiera** de estos topes:
| Concepto | Tope |
|---|---|
| Patrimonio bruto a 31 de diciembre | **Más de 4.500 UVT** |
| Ingresos brutos | **1.400 UVT o más** |
| Consumos con tarjeta de crédito | Más de 1.400 UVT |
| Compras y consumos totales | Más de 1.400 UVT |
| Consignaciones, depósitos o inversiones | Más de 1.400 UVT |
También declara quien sea **responsable de IVA**. El valor de la UVT lo fija cada año la DIAN por resolución.
- **Residencia fiscal (Art. 10 E.T.):** permanecer en el país **más de 183 días calendario** (continuos o discontinuos) en un periodo de 365 días.
- Declaración en **formulario 210**; vencimientos según los últimos dígitos del NIT.

### 2. IVA
- Tarifa general **19 %**; tarifa diferencial **5 %**.
- **Bienes exentos:** gravados a tarifa 0 %; el productor **tiene derecho a devolución** del IVA pagado en sus insumos.
- **Bienes excluidos:** **no causan** IVA; quien los vende **no** tiene derecho a devolución (el IVA pagado se vuelve costo).
- **No responsables de IVA (Art. 437 par. 3)** — personas naturales que cumplan **todas** estas condiciones:
  - ingresos brutos totales de la actividad **inferiores a 3.500 UVT** en el año anterior o en el año en curso;
  - **máximo un establecimiento** de comercio, oficina, sede o local;
  - no ser usuario aduanero;
  - no realizar actividades bajo franquicia, concesión o regalía;
  - no celebrar en el año contratos de venta de bienes o prestación de servicios gravados por valor individual igual o superior a 3.500 UVT;
  - consignaciones, depósitos o inversiones financieras inferiores a 3.500 UVT.

### 3. Régimen SIMPLE (Arts. 903-916 E.T.)
- Opcional; tope de ingresos brutos **inferiores a 100.000 UVT**.
- Integra renta, impuesto nacional al consumo (cuando aplica) y el ICA consolidado.
- **Anticipos bimestrales** y una **declaración anual consolidada** (formulario 260).
- No están sujetos a retención en la fuente ni deben practicarla, **salvo** la de pagos laborales (Art. 911 E.T.)."""),
        ("Orientación aduanera y cambiaria básica", "Decreto 1165 de 2019 · Ley 9 de 1991 · Decreto Ley 2245 de 2011 · Código Penal Arts. 319-321 · Ley 1762 de 2015",
         """### 1. Aduanas (DIAN = autoridad aduanera)
- **Decreto 1165 de 2019:** régimen de aduanas. Regímenes principales: **importación, exportación y tránsito**.
- **Viajeros:** quien ingrese o salga del país con dinero en efectivo o títulos por **más de USD 10.000** (o su equivalente) debe declararlo en la **declaración de equipaje**.
- **Corte normativo de la Guía DIAN 2676:** la **Ley 2586 de 2026** (nuevo régimen sancionatorio aduanero) es del **19 de junio de 2026**, fecha del corte, así que queda por fuera. Prioriza conceptos que no cambian: regímenes, declarante, control aduanero y contrabando.

### 2. Contrabando (Ley 1762 de 2015 — ley anticontrabando)
- **Contrabando (Art. 319 C.P.):** introducir o extraer mercancías del territorio aduanero nacional **por lugares no habilitados**, u ocultándolas, disimulándolas o sustrayéndolas del control aduanero (**contrabando abierto**).
- **Fraude aduanero (Art. 321 C.P.)** y **contrabando técnico:** la mercancía sí se presenta a la aduana, pero con declaraciones falsas (**subfacturación**, origen o clasificación arancelaria falsos) para pagar menos tributos.
- **Favorecimiento y facilitación del contrabando (Art. 320 C.P.):** poseer, tener, transportar, almacenar o comercializar mercancías de contrabando.

### 3. Régimen cambiario
- **Ley 9 de 1991:** ley marco. La **Junta Directiva del Banco de la República** es la autoridad cambiaria (regula).
- **Mercado cambiario** (canalización obligatoria por intermediarios autorizados): importaciones y exportaciones de bienes, endeudamiento externo, inversiones internacionales, entre otras. **Mercado libre:** las demás operaciones.
- **Control y vigilancia:**
  - **DIAN:** operaciones de cambio relativas a **importación y exportación de bienes y servicios**, sus gastos asociados y financiación, y los **profesionales de compra y venta de divisas** (casas de cambio). Régimen sancionatorio: **Decreto Ley 2245 de 2011**.
  - **Superintendencia de Sociedades:** inversión internacional y endeudamiento externo, entre otros.
  - **Superintendencia Financiera:** intermediarios del mercado cambiario vigilados (bancos, etc.)."""),
    ],
    4: [
        ("Dirección y administración de canales de servicio", "Ley 1712 de 2014 · Resolución MinTIC 1519 de 2020 · CPACA Arts. 5 y 7",
         """### 1. Mapa de canales
| Canal | Ejemplos | Ventaja |
|---|---|---|
| Presencial | Puntos de contacto, ventanilla, cita previa | Trámites que exigen validación de identidad |
| Telefónico | Contact center | Orientación rápida |
| Virtual | Portal, servicios en línea, chat, videoatención, redes | Autogestión 24/7 |
| Escrito | Correspondencia, PQRSFD web | Trazabilidad formal |

### 2. Administrar canales = medir y decidir
Indicadores clave:
- **Tiempo de espera** y **tiempo de atención**.
- **Nivel de servicio** (porcentaje de atenciones dentro del tiempo objetivo).
- **Tasa de abandono** (usuarios que se van sin ser atendidos).
- **Resolución en primer contacto.**
- **Satisfacción** del usuario.

Decisiones típicas ante picos de demanda (vencimientos de renta, campañas):
- Ampliar la oferta de citas y **reasignar personal** a los canales congestionados.
- Habilitar filtros de orientación y **promover la autogestión** en canales virtuales, **sin cerrar** el canal presencial.
- Planes de **contingencia** ante caídas del sistema (informar, pre-revisar documentos, reprogramar con prioridad).

### 3. Accesibilidad e inclusión
- Atención **preferente** (CPACA Art. 5 num. 6).
- **Ajustes razonables** para personas con discapacidad; para personas sordas, el **Centro de Relevo** (servicio del Estado colombiano que permite la comunicación con intérprete de lengua de señas).
- **Resolución MinTIC 1519 de 2020:** estándares de publicación y accesibilidad web de la información de las entidades."""),
    ],
    5: [
        ("Gestión documental aplicada", "Ley 594 de 2000 · Decreto 1080 de 2015 · Acuerdo AGN 060 de 2001 · Acuerdo AGN 001 de 2024",
         """### 1. Instrumentos archivísticos
- **TRD — Tabla de Retención Documental:** series, subseries y tipos documentales con su **tiempo de retención** en cada fase y su **disposición final**.
- **TVD — Tabla de Valoración Documental:** se aplica a los **fondos acumulados** (documentos producidos antes de tener TRD).
- **PGD — Programa de Gestión Documental** y **PINAR — Plan Institucional de Archivos**.
- **FUID — Formato Único de Inventario Documental:** se usa en las transferencias y en el inventario.
- **Acuerdo AGN 001 de 2024:** Acuerdo Único de la función archivística.

### 2. Principios archivísticos
- **Procedencia:** los documentos se conservan agrupados según la dependencia que los produjo.
- **Orden original:** se respeta el orden en que se produjeron los documentos dentro del expediente (cronológico).

### 3. Transferencias
- **Primaria:** del **archivo de gestión al archivo central**, cuando se cumple el tiempo de retención en gestión según la TRD.
- **Secundaria:** del **archivo central al archivo histórico**, para los documentos de conservación permanente.

### 4. Disposición final (según TRD)
Conservación total · Selección (muestreo) · Eliminación · Medio técnico (digitalización o microfilmación).
**Eliminación:** solo cuando la TRD/TVD lo establece, con aprobación del **Comité Institucional de Gestión y Desempeño**, levantando un acta y publicando los inventarios. **Nunca** por decisión individual.

### 5. Comunicaciones oficiales (Acuerdo AGN 060 de 2001)
- Toda comunicación oficial recibida o enviada se **radica** en la **ventanilla única de correspondencia** con un **número consecutivo**, fecha y hora.
- Se controlan los tiempos de respuesta desde la radicación."""),
        ("MIPG en detalle: políticas, control interno y líneas de defensa", "Decreto 1499 de 2017 (modifica el Decreto 1083 de 2015) · Manual Operativo MIPG",
         """### 1. Las 7 dimensiones
1. **Talento Humano** (corazón del modelo)
2. Direccionamiento Estratégico y Planeación
3. **Gestión con Valores para Resultados** (incluye Servicio al Ciudadano, Trámites, Participación y Gobierno Digital)
4. Evaluación de Resultados
5. Información y Comunicación (incluye Transparencia y Gestión Documental)
6. Gestión del Conocimiento y la Innovación
7. **Control Interno**

### 2. Políticas de gestión y desempeño (selección)
Planeación institucional · Gestión presupuestal y eficiencia del gasto · Compras y contratación pública · Talento humano · **Integridad** · **Transparencia, acceso a la información y lucha contra la corrupción** · Fortalecimiento organizacional · **Servicio al ciudadano** · Participación ciudadana · **Racionalización de trámites** · **Gestión documental** · Gobierno digital · Seguridad digital · Defensa jurídica · Mejora normativa · Gestión del conocimiento · Control interno · Seguimiento y evaluación del desempeño · Gestión de la información estadística.

### 3. Control interno: MECI y esquema de líneas de defensa
Componentes del MECI: **ambiente de control, evaluación del riesgo, actividades de control, información y comunicación, actividades de monitoreo**.
| Línea | Quién | Qué hace |
|---|---|---|
| **Estratégica** | Alta dirección y Comité Institucional de Coordinación de Control Interno | Define el marco y las políticas de riesgo |
| **Primera** | Gerentes públicos y **líderes de proceso** y sus equipos | Ejecutan los controles **en el día a día** |
| **Segunda** | Jefes de planeación, coordinadores de riesgo, supervisores | Monitorean y asesoran sobre los controles |
| **Tercera** | **Oficina de Control Interno** | Evaluación **independiente** |

### 4. Medición
**FURAG** (Formulario Único de Reporte de Avances de la Gestión): mide el desempeño institucional de las entidades."""),
        ("Protección de datos personales (Ley 1581 de 2012)", "Ley 1581 de 2012 · Constitución Art. 15",
         """### Principios
Legalidad · Finalidad · Libertad (autorización previa, expresa e informada) · Veracidad · Transparencia · Acceso y circulación restringida · Seguridad · Confidencialidad.

### Derechos del titular
Conocer, **actualizar y rectificar** sus datos; solicitar prueba de la autorización; ser informado del uso; presentar quejas ante la **Superintendencia de Industria y Comercio**; revocar la autorización o pedir la supresión (cuando no exista un deber legal de conservarlos).

### Términos
| Trámite | Plazo |
|---|---|
| **Consulta** | Máximo **10 días hábiles** (prorrogables hasta 5 días hábiles más, informando el motivo) |
| **Reclamo** | Máximo **15 días hábiles** (prorrogables hasta 8 días hábiles más, informando el motivo) |

**Datos sensibles:** los que afectan la intimidad o pueden generar discriminación (origen racial, orientación política, convicciones religiosas, salud, vida sexual, biométricos). Tienen protección reforzada."""),
    ],
    6: [
        ("Cómo se califican las pruebas Comportamental y de Integridad", "Guía de Orientación al Aspirante — Proceso de Selección DIAN 2676",
         """### Formato real del examen
- Las pruebas **Comportamental (15 %)** y **de Integridad (10 %)** usan una **escala Likert de 4 opciones**: Totalmente en desacuerdo · En desacuerdo · De acuerdo · Totalmente de acuerdo.
- **Novedad de DIAN 2676:** la Guía incluye **dos subescalas de control** para medir respuestas **exageradamente favorables**. Según la Guía, ese análisis determina **qué ítems entran en la calificación**.

### Estrategia
- Lee el matiz de cada afirmación; **no marques extremos por reflejo**.
- Sé **consistente**: la misma idea aparece formulada de distintas maneras.
- Responde con un apego **realista** a los principios del servicio público (nadie es "perfecto" en todo).
- Los resultados Comportamental y de Integridad solo se publican a quienes superan el mínimo de la prueba Funcional (70/100).

> En esta app, las preguntas comportamentales y de integridad se practican en formato A/B/C para entrenar el criterio: identificar la conducta que mejor refleja la competencia o el valor."""),
    ],
}

# =============================================================================
# BANCO DE PREGUNTAS AMPLIADO (juicio situacional · 3 opciones · 1 correcta)
# =============================================================================
def _q(module, category, case, question, correct, options, explanation, legal):
    return {
        "module": module, "category": category, "case_study": case,
        "question_text": question, "correct": correct, "options": options,
        "explanation": explanation, "legal_reference": legal,
    }

EXTRA_QUESTIONS = [
    # ---------------------------- MÓDULO 1: RUT ----------------------------
    _q(1, "Funcional",
       "Una diseñadora gráfica que va a empezar a prestar servicios como independiente le dice al Analista IV que primero quiere facturar su primer mes de trabajo y que, si le va bien, se inscribirá en el RUT más adelante.",
       "¿Qué orientación debe darle el Analista IV conforme al Estatuto Tributario?",
       "A",
       ["Que la inscripción en el RUT debe hacerse antes de iniciar la actividad económica, porque inscribirse después es extemporáneo y genera la sanción del artículo 658-3 del E.T.",
        "Que tiene plazo de un año desde el inicio de la actividad para inscribirse sin ninguna consecuencia.",
        "Que si expide facturas en papel no necesita inscribirse en el RUT."],
       "La opción A es la correcta: el RUT es el mecanismo único de identificación de los obligados (Art. 555-2 E.T.) y la inscripción debe ser previa al inicio de la actividad; la inscripción tardía es extemporánea y sancionable (Art. 658-3 E.T.). La opción B se inventa un plazo de gracia que no existe. La opción C confunde la facturación con la obligación de inscribirse, que es independiente.",
       "Estatuto Tributario Arts. 555-2 y 658-3"),
    _q(1, "Funcional",
       "Durante una cita presencial de inscripción en el RUT, el Analista IV observa que la fotografía y la firma del documento de identidad no coinciden con la persona que lo presenta, quien insiste en que se trata de él y tiene prisa.",
       "En desarrollo de la función de garantizar la veracidad y confiabilidad del RUT, ¿cuál es la actuación correcta?",
       "C",
       ["Formalizar la inscripción y dejar una observación en el sistema para que otra dependencia revise después.",
        "Retener el documento de identidad y retener físicamente a la persona hasta que llegue la Policía.",
        "Abstenerse de formalizar el trámite, aplicar el protocolo interno de validación de identidad y reportar la inconsistencia según el procedimiento."],
       "La opción C es la correcta: ante indicios de suplantación, el servidor no debe formalizar el registro y debe seguir el protocolo de validación y reporte, protegiendo la confiabilidad del RUT. La opción A permite un registro posiblemente fraudulento. La opción B es una actuación arbitraria que excede las funciones del servidor.",
       "Ficha CC-AU-2010 (función esencial 4) · DUR 1625 de 2016"),
    _q(1, "Funcional",
       "Un comerciante de Arauca cambió hace 20 días su actividad principal de venta de ropa a venta de electrodomésticos. Pregunta si debe hacer algo con su RUT o si la DIAN lo actualiza sola.",
       "¿Cuál es la orientación correcta?",
       "B",
       ["No debe hacer nada: el RUT solo se actualiza cuando presenta la declaración de renta.",
        "Debe actualizar la actividad económica dentro del mes siguiente al cambio; puede hacerlo en línea con su usuario e IFE o por el canal presencial.",
        "La DIAN actualiza automáticamente toda actividad económica, así que no es obligación del contribuyente."],
       "La opción B es la correcta: la actualización a solicitud de parte es obligación del inscrito y debe hacerse dentro del mes siguiente al hecho que la origina; de lo contrario, incurre en la sanción por desactualización (Art. 658-3 E.T.). La opción A inventa una regla. La opción C confunde la actualización de oficio (excepcional) con el deber del contribuyente.",
       "Estatuto Tributario Art. 658-3 · DUR 1625 de 2016 Art. 1.6.1.2.14"),
    _q(1, "Funcional",
       "El liquidador de una sociedad ya liquidada solicita la cancelación del RUT. Al revisar, el Analista IV encuentra que la sociedad tiene omisa la declaración de IVA de un periodo no prescrito.",
       "¿Cómo debe proceder?",
       "A",
       ["Informar que la cancelación procede una vez se verifique el cumplimiento de las obligaciones, por lo que primero debe subsanarse la omisión.",
        "Cancelar el RUT de inmediato, porque la liquidación de la sociedad extingue automáticamente sus obligaciones tributarias.",
        "Suspender el RUT de manera indefinida y archivar la solicitud sin respuesta."],
       "La opción A es la correcta: la cancelación del RUT exige verificar previamente que no existan obligaciones pendientes, como declaraciones omisas en periodos no prescritos. La opción B es falsa porque la liquidación no extingue las obligaciones tributarias causadas. La opción C deja la solicitud sin respuesta, lo que vulnera el derecho de petición.",
       "DUR 1625 de 2016 · Ley 1755 de 2015"),

    # ---------------------------- MÓDULO 2: PQRSF ----------------------------
    _q(2, "Funcional",
       "Un ciudadano radica una petición para que la DIAN le corrija un dato, pero no adjunta el documento indispensable para resolverla ni indica qué periodo debe corregirse.",
       "Según la Ley 1755 de 2015, ¿qué debe hacer la entidad?",
       "A",
       ["Requerir al peticionario dentro de los 10 días siguientes a la radicación para que la complete en el término de un mes; si no lo hace, se entiende que desistió.",
        "Archivarla de inmediato por estar incompleta, sin comunicar nada al ciudadano.",
        "Esperar el día 15 y negar la petición por falta de requisitos."],
       "La opción A es la correcta según el Art. 17 de la Ley 1755 de 2015: si la petición está incompleta, la autoridad requiere al peticionario dentro de los 10 días siguientes para que la complete en un mes (prorrogable); si no lo hace, opera el desistimiento tácito. La opción B omite el requerimiento obligatorio. La opción C niega por un defecto que la ley ordena subsanar.",
       "Ley 1755 de 2015 Art. 17"),
    _q(2, "Funcional",
       "El día 12 de un término de 15 días, el Analista IV comprueba que una petición compleja exige consultar información de tres seccionales y no podrá responderse a tiempo.",
       "¿Cuál es la actuación ajustada a la ley?",
       "C",
       ["Responder cuando la información esté lista, sin informar nada, porque la complejidad justifica la demora.",
        "Ampliar el término unilateralmente a tres meses y aplicar el silencio negativo.",
        "Informar al peticionario antes del vencimiento los motivos de la demora y el plazo razonable de respuesta, que no puede exceder el doble del término inicial."],
       "La opción C es la correcta: el parágrafo del Art. 14 de la Ley 1755 de 2015 permite ampliar el plazo informando al interesado antes de que venza, con los motivos y un plazo razonable que no exceda el doble del inicial. La opción A vulnera el derecho de petición. La opción B confunde el silencio negativo del Art. 83 CPACA con la ampliación del término.",
       "Ley 1755 de 2015 Art. 14 parágrafo"),
    _q(2, "Funcional",
       "Una usuaria escribe por la sede electrónica que el funcionario que la atendió ayer en ventanilla le habló con gritos y se negó a recibirle sus documentos.",
       "¿Cómo debe clasificarse y tramitarse este requerimiento?",
       "B",
       ["Como sugerencia, porque propone que la atención mejore.",
        "Como queja contra un servidor, darle trámite y remitirla a la dependencia de Control Disciplinario Interno, informando a la usuaria.",
        "Rechazarla porque la DIAN no puede investigar a sus propios funcionarios."],
       "La opción B es la correcta: la manifestación de inconformidad por la conducta de un servidor es una queja; debe tramitarse y ponerse en conocimiento de Control Disciplinario Interno. La opción A clasifica mal el requerimiento y cambia su ruta. La opción C es falsa: la entidad cuenta con control disciplinario interno.",
       "Ley 1755 de 2015 · Ley 1474 de 2011 Art. 76 · Ley 1952 de 2019"),
    _q(2, "Funcional",
       "Un ciudadano presenta por cuarta vez una petición idéntica a otras tres que la DIAN ya resolvió de fondo y que le fueron notificadas en debida forma.",
       "¿Qué permite la Ley 1755 de 2015?",
       "A",
       ["Remitirse a las respuestas anteriores, salvo que se trate de derechos imprescriptibles o de peticiones que no fueron resueltas de fondo.",
        "Imponer al ciudadano una multa por abusar del derecho de petición.",
        "Abstenerse de responder, porque las peticiones reiterativas no generan ninguna obligación."],
       "La opción A es la correcta según el Art. 19 de la Ley 1755: frente a peticiones reiterativas ya resueltas, la autoridad puede remitirse a las respuestas anteriores. La opción B inventa una sanción. La opción C es incorrecta porque igualmente se debe dar respuesta, aunque sea remitiendo a la anterior.",
       "Ley 1755 de 2015 Art. 19"),
    _q(2, "Funcional",
       "Una periodista solicita por escrito, para una investigación sobre recaudo, las cifras agregadas de recaudo de IVA de la seccional en el último año. No pide información de ningún contribuyente en particular.",
       "¿Cómo debe tramitarse la solicitud?",
       "C",
       ["Negarla por la reserva tributaria del Art. 583 del E.T.",
        "Tramitarla como consulta jurídica con plazo de 30 días.",
        "Tramitarla preferencialmente por ser de una periodista en ejercicio de su actividad y entregar la información pública agregada."],
       "La opción C es la correcta: el Art. 20 de la Ley 1755 ordena dar trámite preferencial a las peticiones de periodistas para el ejercicio de su actividad, y las cifras agregadas de recaudo son información pública. La opción A aplica mal la reserva del Art. 583, que protege las declaraciones individuales, no las estadísticas agregadas. La opción B clasifica mal la petición.",
       "Ley 1755 de 2015 Art. 20 · Ley 1712 de 2014"),

    # ---------------------------- MÓDULO 3: TACI ----------------------------
    _q(3, "Funcional",
       "Una persona natural residente le cuenta al Analista IV que en el año gravable tuvo un patrimonio bruto equivalente a 3.000 UVT e ingresos brutos por 1.600 UVT. No es responsable de IVA.",
       "¿Está obligada a declarar renta?",
       "B",
       ["No, porque su patrimonio bruto no supera las 4.500 UVT.",
        "Sí, porque sus ingresos brutos superan el tope de 1.400 UVT; basta con superar uno solo de los topes.",
        "Solo si es comerciante inscrito en el registro mercantil."],
       "La opción B es la correcta: la persona natural debe declarar si supera cualquiera de los topes. Los ingresos brutos de 1.600 UVT superan el tope de 1.400 UVT, aunque el patrimonio esté por debajo de 4.500 UVT. La opción A exige cumplir todos los topes, cuando basta con superar uno. La opción C introduce un requisito inexistente.",
       "Estatuto Tributario Arts. 592 a 594-3"),
    _q(3, "Funcional",
       "El dueño de una pequeña tienda (persona natural), con un único local, ingresos brutos del año de 2.000 UVT, que no es usuario aduanero ni opera franquicias y no celebra contratos grandes, pregunta si debe cobrar IVA.",
       "¿Cuál es la orientación correcta?",
       "A",
       ["Puede ser no responsable de IVA si cumple todas las condiciones del parágrafo 3 del Art. 437 del E.T., entre ellas tener ingresos brutos inferiores a 3.500 UVT y un solo establecimiento.",
        "Todos los comerciantes son responsables de IVA desde el primer peso vendido.",
        "Su responsabilidad de IVA depende únicamente de si tiene o no RUT."],
       "La opción A es la correcta: el parágrafo 3 del Art. 437 E.T. fija las condiciones para ser no responsable (ingresos inferiores a 3.500 UVT, máximo un establecimiento, no ser usuario aduanero, entre otras), y deben cumplirse todas. La opción B desconoce el régimen de no responsables. La opción C confunde la inscripción en el RUT con la responsabilidad del impuesto.",
       "Estatuto Tributario Art. 437 parágrafo 3"),
    _q(3, "Funcional",
       "Un productor pregunta qué diferencia práctica hay entre que su producto sea 'exento' o 'excluido' de IVA.",
       "¿Cuál es la explicación técnicamente correcta?",
       "C",
       ["Son sinónimos: en ambos casos el producto no paga IVA y no hay ninguna otra consecuencia.",
        "El bien excluido está gravado a tarifa 0 % con derecho a devolución, y el exento no causa el impuesto.",
        "El bien exento está gravado a tarifa 0 % y el productor tiene derecho a devolución del IVA pagado en insumos; el excluido no causa IVA y no da derecho a devolución."],
       "La opción C es la correcta: los bienes exentos son gravados a tarifa cero, con derecho a devolución, mientras que los excluidos no causan IVA y el impuesto pagado en insumos se vuelve mayor costo. La opción A ignora la diferencia en devoluciones. La opción B invierte los conceptos.",
       "Estatuto Tributario Arts. 420, 424 y 477"),
    _q(3, "Funcional",
       "Un viajero que va a salir del país por el aeropuerto pregunta si puede llevar USD 15.000 en efectivo sin hacer ningún trámite.",
       "¿Cuál es la orientación correcta?",
       "B",
       ["Sí, no hay ningún límite para llevar divisas en efectivo.",
        "Debe declarar el dinero en la declaración de equipaje, porque supera el equivalente a USD 10.000.",
        "Debe cambiar obligatoriamente los dólares a pesos en el aeropuerto antes de salir."],
       "La opción B es la correcta: el ingreso o la salida de dinero en efectivo por más de USD 10.000 (o su equivalente) debe declararse ante la DIAN en la declaración de equipaje. La opción A desconoce el control aduanero y cambiario. La opción C impone una obligación inexistente.",
       "Decreto 1165 de 2019 (régimen de viajeros) · régimen cambiario"),
    _q(3, "Funcional",
       "Un importador pregunta qué entidad controla que haya canalizado por el mercado cambiario los pagos al exterior de sus importaciones de bienes.",
       "¿Qué debe responder el Analista IV?",
       "A",
       ["La DIAN, que ejerce el control cambiario de las operaciones de importación y exportación de bienes y servicios.",
        "El Banco de la República, que impone directamente las sanciones a los importadores.",
        "La Superintendencia Financiera, que vigila a todos los importadores del país."],
       "La opción A es la correcta: la DIAN controla y vigila el régimen cambiario en las operaciones de importación y exportación de bienes y servicios (régimen sancionatorio del Decreto Ley 2245 de 2011). La opción B confunde la función reguladora de la Junta Directiva del Banco de la República con el control. La opción C es incorrecta: la Superintendencia Financiera vigila a los intermediarios del mercado cambiario, no a los importadores.",
       "Ley 9 de 1991 · Decreto Ley 2245 de 2011"),
    _q(3, "Funcional",
       "Una empresa importa televisores por el puerto habilitado de Buenaventura y presenta la declaración de importación, pero declara un precio muy inferior al real (subfacturación) para pagar menos aranceles e IVA.",
       "¿Cómo se denomina técnicamente esta conducta?",
       "C",
       ["Contrabando abierto, porque las mercancías ingresaron al país.",
        "Elusión fiscal legítima, porque se usó un puerto habilitado.",
        "Contrabando técnico (fraude aduanero): la mercancía se presenta a la aduana, pero con información falsa para pagar menos tributos."],
       "La opción C es la correcta: cuando la mercancía sí se somete al control aduanero pero con declaraciones falsas (subfacturación, origen o clasificación falsos), se habla de contrabando técnico o fraude aduanero (Art. 321 C.P.). La opción A corresponde a introducir la mercancía por lugares no habilitados o eludiendo el control. La opción B es falsa: la subfacturación es ilegal.",
       "Código Penal Arts. 319 y 321 · Ley 1762 de 2015"),
    _q(3, "Funcional",
       "El dueño de un almacén, facturador electrónico, le vende a una persona que no recibe facturas por correo electrónico. Pregunta si con imprimir la factura en papel ya cumplió, aunque no la haya enviado a validación de la DIAN.",
       "¿Cuál es la orientación correcta?",
       "B",
       ["Sí, la impresión en papel reemplaza la validación previa cuando el comprador no tiene correo.",
        "No: la factura electrónica debe validarse previamente por la DIAN; al comprador que no la recibe electrónicamente se le entrega la representación gráfica, que no reemplaza la validación.",
        "Debe dejar de facturar a ese cliente hasta que tenga correo electrónico."],
       "La opción B es la correcta: la factura electrónica es el documento validado previamente por la DIAN; la representación gráfica (física o digital) se entrega al adquirente que no la recibe electrónicamente, pero no reemplaza la validación. La opción A desconoce la validación previa. La opción C impone una restricción ilegal a la venta.",
       "Estatuto Tributario Art. 616-1 · Resolución DIAN 000165 de 2023"),

    # ---------------------------- MÓDULO 4: CANALES ----------------------------
    _q(4, "Funcional",
       "En plena temporada de renta, el tablero de indicadores del punto de contacto muestra un tiempo de espera de 2 horas y un 30 % de abandono. El jefe pide al Analista IV una propuesta inmediata.",
       "¿Cuál es la propuesta más adecuada para administrar el canal?",
       "C",
       ["Cerrar el canal presencial durante la temporada y atender únicamente por medios virtuales.",
        "Atender en orden de llegada sin cita ni medición, para no complicar el proceso.",
        "Ampliar la oferta de citas y reasignar personal a las horas pico, habilitar un filtro de orientación y promover la autogestión virtual, manteniendo el canal presencial y midiendo los resultados."],
       "La opción C es la correcta: administrar canales implica usar los indicadores (tiempo de espera, abandono) para ajustar capacidad, gestionar la demanda y promover la autogestión sin dejar de prestar el servicio presencial. La opción A crea una barrera de acceso para quienes no usan medios digitales. La opción B renuncia a la gestión y a la medición.",
       "Política de Servicio al Ciudadano (MIPG) · CPACA Art. 7"),
    _q(4, "Funcional",
       "Una persona sorda llega sin acompañante al punto de contacto para actualizar su RUT. Se comunica mediante lengua de señas.",
       "¿Qué debe hacer el Analista IV?",
       "A",
       ["Brindarle atención preferente con ajustes razonables, por ejemplo usando el Centro de Relevo con intérprete o la comunicación escrita, hasta completar el trámite.",
        "Pedirle que regrese otro día con un familiar que le sirva de intérprete.",
        "Indicarle que radique una petición escrita y espere la respuesta en 15 días."],
       "La opción A es la correcta: las personas con discapacidad tienen derecho a atención especial y preferente (Art. 5 num. 6 CPACA) y la entidad debe hacer ajustes razonables, como el Centro de Relevo. Las opciones B y C trasladan la carga al ciudadano y crean barreras de acceso.",
       "Ley 1437 de 2011 Art. 5 num. 6 · Ley 1618 de 2013"),
    _q(4, "Funcional",
       "Por el chat institucional, un usuario que no se ha autenticado pide que le confirmen el valor del impuesto que liquidó en su declaración de renta del año pasado, porque perdió la copia.",
       "¿Cómo debe responder el Analista IV?",
       "B",
       ["Darle el valor de inmediato, porque el chat es un canal oficial de la entidad.",
        "Abstenerse de suministrar datos de la declaración por estar amparados por reserva, y orientarlo para consultarlos con su usuario y firma en los servicios en línea o por un canal donde se verifique su identidad.",
        "Pedirle que envíe su contraseña por el chat para ingresar por él a su cuenta."],
       "La opción B es la correcta: la información de las declaraciones tiene reserva (Art. 583 E.T.) y solo se entrega al titular o a su apoderado debidamente identificado, por canales que permitan verificar su identidad. La opción A vulnera la reserva. La opción C es una práctica insegura y contraria a la protección de credenciales.",
       "Estatuto Tributario Art. 583 · Ley 1581 de 2012"),

    # ---------------------------- MÓDULO 5: TRANSPARENCIA / DOCUMENTAL / MIPG ----------------------------
    _q(5, "Funcional",
       "Un ciudadano solicita la relación de contratos suscritos por la Dirección Seccional durante el último año. El funcionario que recibe la solicitud le pide que explique para qué quiere la información y le anuncia un cobro por la búsqueda.",
       "¿Cuál es la actuación correcta según la Ley 1712 de 2014?",
       "A",
       ["Entregar la información por ser pública, sin exigir que el solicitante justifique su interés y cobrando a lo sumo el costo de reproducción.",
        "Cobrar una tarifa por el tiempo de búsqueda del funcionario.",
        "Exigir que el ciudadano justifique por escrito el uso que dará a la información antes de tramitarla."],
       "La opción A es la correcta: la información sobre contratación es pública; el acceso no exige motivar la solicitud y rige el principio de gratuidad (solo se puede cobrar el costo de reproducción). La opción B viola la gratuidad. La opción C impone un requisito que la ley no exige.",
       "Ley 1712 de 2014 (principios de máxima publicidad y gratuidad)"),
    _q(5, "Funcional",
       "Un usuario pregunta durante cuánto tiempo puede la entidad mantener en reserva un documento clasificado como información reservada por razones de defensa nacional.",
       "Según la Ley 1712 de 2014, ¿cuál es la respuesta correcta?",
       "C",
       ["De manera indefinida, mientras la entidad lo considere necesario.",
        "Máximo cinco (5) años, sin excepción.",
        "Por un periodo que no puede exceder de quince (15) años."],
       "La opción C es la correcta: el Art. 22 de la Ley 1712 de 2014 establece que la reserva de la información pública reservada no puede extenderse por más de 15 años. La opción A desconoce ese límite temporal. La opción B cita un término inexistente.",
       "Ley 1712 de 2014 Art. 22"),
    _q(5, "Funcional",
       "Un ciudadano entrega personalmente al Analista IV una carta dirigida a la Seccional con una solicitud. El funcionario está muy ocupado y piensa guardarla en su escritorio para revisarla después.",
       "Conforme a la gestión documental de las comunicaciones oficiales, ¿qué debe hacerse?",
       "B",
       ["Guardarla en el escritorio y radicarla cuando tenga tiempo.",
        "Radicarla en la ventanilla única de correspondencia, asignándole número consecutivo, fecha y hora, para controlar los términos de respuesta.",
        "Responderle informalmente por WhatsApp sin dejar registro, para agilizar."],
       "La opción B es la correcta: las comunicaciones oficiales se radican en la ventanilla única con número consecutivo, fecha y hora (Acuerdo AGN 060 de 2001); desde ahí se cuentan los términos. La opción A pone en riesgo el cumplimiento del término y la trazabilidad. La opción C carece de trazabilidad y formalidad.",
       "Acuerdo AGN 060 de 2001 · Ley 594 de 2000"),
    _q(5, "Funcional",
       "El jefe de la División de Asistencia al Usuario identifica en su proceso el riesgo de que se venzan peticiones y establece una revisión diaria del tablero de términos con su equipo.",
       "Según el esquema de líneas de defensa del MIPG, ¿en qué línea actúa?",
       "A",
       ["Primera línea de defensa: los líderes de proceso y sus equipos ejecutan los controles en el día a día.",
        "Tercera línea de defensa: la evaluación independiente.",
        "Línea estratégica: la definición de las políticas de riesgo de toda la entidad."],
       "La opción A es la correcta: la primera línea la conforman los gerentes públicos y los líderes de proceso, responsables de los controles en la operación diaria. La tercera línea corresponde a la Oficina de Control Interno (evaluación independiente). La línea estratégica es la alta dirección y el Comité Institucional de Coordinación de Control Interno.",
       "Decreto 1499 de 2017 · Manual Operativo MIPG (Dimensión 7)"),
    _q(5, "Funcional",
       "En una capacitación preguntan en cuál dimensión del MIPG se ubica la política de Servicio al Ciudadano.",
       "¿Cuál es la respuesta correcta?",
       "B",
       ["Dimensión 1 — Talento Humano.",
        "Dimensión 3 — Gestión con Valores para Resultados.",
        "Dimensión 7 — Control Interno."],
       "La opción B es la correcta: la política de Servicio al Ciudadano, junto con Racionalización de Trámites, Participación Ciudadana y Gobierno Digital, hace parte de la Dimensión 3 'Gestión con Valores para Resultados', en su perspectiva de relación Estado-ciudadano. Las dimensiones 1 y 7 tratan el talento humano y el control interno.",
       "Decreto 1499 de 2017 · Manual Operativo MIPG"),
    _q(5, "Funcional",
       "Una ciudadana solicita por escrito, como titular, conocer qué datos personales de contacto tiene registrados la entidad sobre ella.",
       "Conforme a la Ley 1581 de 2012, ¿en qué término debe responderse esta consulta?",
       "C",
       ["En 30 días hábiles, como las consultas jurídicas.",
        "En 3 meses, porque aplica el silencio negativo.",
        "En un máximo de 10 días hábiles, previa verificación de que quien consulta es la titular de los datos."],
       "La opción C es la correcta: el Art. 14 de la Ley 1581 de 2012 fija un término máximo de 10 días hábiles para las consultas del titular (prorrogable hasta 5 días hábiles informando el motivo). La opción A confunde con las consultas de la Ley 1755. La opción B confunde con el silencio administrativo negativo.",
       "Ley 1581 de 2012 Art. 14"),

    # ---------------------------- MÓDULO 6: COMPORTAMENTAL / INTEGRIDAD ----------------------------
    _q(6, "Comportamental",
       "El Analista IV terminó su agenda de citas antes de lo previsto. Su compañera de módulo tiene una fila de seis usuarios represados por un trámite complejo de RUT.",
       "¿Qué conducta refleja mejor la competencia de Trabajo en Equipo?",
       "B",
       ["Aprovechar el tiempo libre para tomar un descanso, porque ya cumplió su meta individual.",
        "Ofrecer apoyo a la compañera, coordinando con ella o con el coordinador para atender parte de los usuarios represados.",
        "Informar al jefe que su compañera es lenta para que tome medidas."],
       "La opción B es la correcta: el trabajo en equipo implica colaborar para alcanzar los objetivos comunes, más allá de la meta individual. La opción A se enfoca solo en lo propio. La opción C no aporta a la solución y deteriora el clima laboral.",
       "Decreto 815 de 2018 · Ficha CC-AU-2010"),
    _q(6, "Comportamental",
       "La DIAN implementa un nuevo aplicativo para el trámite de PQRSFD que cambia por completo la forma de trabajar del equipo. Varios compañeros se quejan y siguen usando el procedimiento anterior.",
       "¿Qué conducta refleja mejor la competencia de Adaptabilidad?",
       "C",
       ["Seguir con el procedimiento anterior mientras el nuevo aplicativo demuestra su utilidad.",
        "Usar el nuevo aplicativo solo cuando el jefe esté supervisando.",
        "Aprender a usar el nuevo aplicativo, aplicarlo y compartir con el equipo las dificultades y las propuestas de mejora."],
       "La opción C es la correcta: la adaptabilidad implica enfrentar los cambios con flexibilidad, aprender y proponer mejoras. Las opciones A y B reflejan resistencia al cambio.",
       "Decreto 815 de 2018 · Ficha CC-AU-2010"),
    _q(6, "Comportamental",
       "Un adulto mayor no entiende por qué debe declarar renta y se muestra confundido con términos como 'patrimonio bruto' y 'UVT'.",
       "¿Qué conducta refleja mejor la competencia de Comunicación Efectiva?",
       "A",
       ["Explicarle con lenguaje claro y ejemplos cotidianos, resumir los pasos y verificar que comprendió, sin afectar la precisión normativa.",
        "Leerle textualmente los artículos del Estatuto Tributario para que no haya errores.",
        "Entregarle un folleto y llamar al siguiente turno para no retrasar la fila."],
       "La opción A es la correcta: comunicar con efectividad es transmitir la información con claridad y asegurarse de que se comprendió. La opción B es precisa pero no se adapta al interlocutor. La opción C omite la verificación de la comprensión.",
       "Ficha CC-AU-2010 · Guía de lenguaje claro"),
    _q(6, "Comportamental",
       "Un usuario pregunta por los efectos de una norma tributaria expedida hace poco y el Analista IV no está seguro de la respuesta.",
       "¿Cuál es la conducta más adecuada?",
       "B",
       ["Dar la respuesta que le parezca más probable para no quedar mal con el usuario.",
        "Consultar las fuentes oficiales (normograma DIAN, doctrina vigente) o al área competente antes de responder, y comunicarle al usuario cuándo y por qué medio recibirá la respuesta.",
        "Decirle que esa norma no aplica para él, para cerrar la consulta."],
       "La opción B es la correcta: refleja orientación al usuario, aprendizaje continuo y responsabilidad, porque garantiza una respuesta correcta y trazable. Las opciones A y C pueden inducir a error al ciudadano y afectar sus derechos.",
       "Ficha CC-AU-2010 · CPACA Art. 3 (principio de responsabilidad)"),
    _q(6, "Integridad",
       "A la ventanilla del Analista IV llega su primo hermano para un trámite de actualización del RUT que presenta una inconsistencia que debe decidirse.",
       "¿Cuál es la actuación íntegra y ajustada a la norma?",
       "A",
       ["Manifestar el conflicto de intereses y solicitar que otro servidor atienda el trámite, siguiendo el procedimiento de impedimentos.",
        "Atenderlo con prioridad y resolver la inconsistencia a su favor, porque conoce bien su caso.",
        "Atenderlo normalmente sin informar nada, porque se trata de un trámite sencillo."],
       "La opción A es la correcta: el parentesco hasta el cuarto grado de consanguinidad (los primos hermanos lo son) es causal de impedimento (Art. 11 CPACA); el servidor debe declararlo y apartarse. Las opciones B y C vulneran los valores de Justicia y Honestidad y el régimen de conflicto de intereses.",
       "Ley 1437 de 2011 Arts. 11 y 12 · Código de Integridad (Justicia)"),
    _q(6, "Integridad",
       "Un amigo del Analista IV le pregunta en una reunión social si cierta empresa de su barrio está siendo investigada por la DIAN, porque piensa hacer negocios con ella.",
       "¿Cuál es la actuación correcta?",
       "C",
       ["Contarle lo que sabe, siempre que no le muestre documentos.",
        "Consultar los sistemas al día siguiente y enviarle la información por mensaje.",
        "Abstenerse de revelar cualquier información de la que tenga conocimiento por razón de su cargo, explicándole que está protegida por reserva."],
       "La opción C es la correcta: revelar información conocida por razón del cargo vulnera la reserva tributaria (Art. 583 E.T.) y puede configurar delitos como la revelación de secreto o la utilización indebida de información privilegiada. Las opciones A y B constituyen faltas graves y posibles delitos.",
       "Estatuto Tributario Art. 583 · Código Penal Arts. 418 y 420"),
    _q(6, "Integridad",
       "Después de resolverle un trámite difícil, una ciudadana agradecida deja en la ventanilla del Analista IV una caja de chocolates con una nota de agradecimiento.",
       "Desde el Código de Integridad, ¿qué debe hacer el servidor?",
       "B",
       ["Aceptarla, porque es un regalo pequeño y el trámite ya se cumplió.",
        "Rechazarla amablemente, agradecer el gesto y explicar que los servidores no pueden recibir regalos por el ejercicio de sus funciones.",
        "Aceptarla y repartirla con el equipo para que nadie se sienta excluido."],
       "La opción B es la correcta: el valor de la Honestidad implica no aceptar regalos ni beneficios por razón del cargo, sin importar su valor. Las opciones A y C normalizan la recepción de dádivas.",
       "Ley 2016 de 2020 (Código de Integridad) · Ley 1952 de 2019"),
    _q(6, "Integridad",
       "El Analista IV se da cuenta de que ayer le dio a un usuario una información equivocada sobre el plazo para actualizar su RUT, lo que podría generarle una sanción.",
       "¿Cuál es la conducta íntegra?",
       "C",
       ["No decir nada, porque nadie se dio cuenta del error.",
        "Esperar a ver si el usuario regresa a reclamar y entonces corregir.",
        "Contactar al usuario por los datos registrados para corregir la información, e informar el error al jefe inmediato para evitar que se repita."],
       "La opción C es la correcta: refleja Honestidad (reconocer el error) y Compromiso (evitar el perjuicio al ciudadano). Las opciones A y B ocultan el error y trasladan el riesgo al usuario.",
       "Código de Integridad (Honestidad y Compromiso)"),
    _q(6, "Integridad",
       "El coordinador le pide al Analista IV cambiar en el sistema la fecha de radicación de una petición para que no figure como respuesta vencida en el informe de gestión.",
       "¿Cuál es la actuación correcta?",
       "A",
       ["Negarse respetuosamente, explicar que alterar la fecha es una falsedad y poner la situación en conocimiento de la instancia competente si la orden persiste.",
        "Cambiar la fecha porque es una orden del superior y la responsabilidad es de él.",
        "Cambiar la fecha solo esta vez y dejar una nota privada como respaldo."],
       "La opción A es la correcta: el deber de obediencia no cubre órdenes manifiestamente ilegales; alterar registros oficiales puede configurar falsedad y una falta disciplinaria. Las opciones B y C hacen al servidor partícipe de la irregularidad.",
       "Constitución Art. 6 · Ley 1952 de 2019 · Código de Integridad (Honestidad)"),

    # ---------------------------- MÓDULO 7: SERVICIO AL CIUDADANO ----------------------------
    _q(7, "Funcional",
       "Para un trámite, un funcionario le exige a un usuario que traiga impreso y autenticado su RUT, aunque la información está disponible en los sistemas de la DIAN.",
       "¿Es correcta esta exigencia?",
       "A",
       ["No. Está prohibido exigir documentos que reposan en la propia entidad; el servidor debe consultar la información en los sistemas.",
        "Sí, porque la autenticación garantiza la veracidad del documento.",
        "Sí, pero solo si el usuario es persona jurídica."],
       "La opción A es la correcta: el Art. 9 del CPACA y el Art. 9 del Decreto Ley 019 de 2012 prohíben exigir documentos que reposan en la entidad. Las opciones B y C imponen un trámite innecesario que la normativa antitrámites prohíbe.",
       "Ley 1437 de 2011 Art. 9 · Decreto Ley 019 de 2012 Art. 9"),
    _q(7, "Funcional",
       "Un ciudadano le pregunta al Analista IV dónde puede conocer sus derechos como usuario de la DIAN y los medios para hacerlos valer.",
       "¿Qué debe responder?",
       "C",
       ["Que esa información es interna y reservada.",
        "Que solo puede conocerla presentando un derecho de petición.",
        "Que la entidad expide y publica la Carta de Trato Digno al usuario, donde se especifican sus derechos y los medios para garantizarlos."],
       "La opción C es la correcta: el Art. 7 num. 5 del CPACA obliga a las autoridades a expedir y hacer visible la Carta de Trato Digno al usuario. Las opciones A y B ponen barreras a una información que debe ser pública y visible.",
       "Ley 1437 de 2011 Art. 7 num. 5"),
    _q(7, "Funcional",
       "Un contribuyente llega muy alterado, levanta la voz y culpa al Analista IV de que su RUT esté suspendido. Otros usuarios observan la situación.",
       "¿Cuál es la actuación más adecuada?",
       "B",
       ["Responderle con el mismo tono para que entienda que no puede gritarle a un servidor público.",
        "Mantener la calma, escucharlo sin interrumpir, reconocer su molestia, explicarle la causa y la forma de levantar la suspensión y, si la agresión persiste, escalar al supervisor.",
        "Negarse a atenderlo y llamar de inmediato a la vigilancia para que lo retiren."],
       "La opción B es la correcta: el protocolo de atención indica serenidad, escucha activa, empatía y foco en la solución, con escalamiento si la agresión continúa. La opción A empeora el conflicto. La opción C omite la atención sin agotar el manejo del conflicto.",
       "Protocolos de Servicio al Ciudadano · CPACA Arts. 6 y 7"),
    _q(7, "Funcional",
       "Durante una asesoría, un comerciante le pide al Analista IV que le 'recomiende' cómo dividir sus ventas entre familiares para no superar los topes y no tener que declarar ni cobrar IVA, aunque el negocio sea el mismo.",
       "¿Cómo debe actuar el servidor?",
       "A",
       ["Orientarlo sobre sus obligaciones y los beneficios legales vigentes, abstenerse de asesorar figuras artificiosas para evitar impuestos y advertirle sus consecuencias.",
        "Explicarle cómo hacerlo, porque la asesoría al contribuyente debe buscar que pague lo menos posible.",
        "Negarse a atenderlo y reportarlo como evasor."],
       "La opción A es la correcta: la asistencia al usuario busca el cumplimiento voluntario; el servidor informa los beneficios legales pero no asesora conductas de abuso (Art. 869 E.T.) o de evasión. La opción B convierte al servidor en partícipe del abuso. La opción C le niega al usuario la orientación sobre sus obligaciones.",
       "Estatuto Tributario Art. 869 · Código de Integridad"),
    _q(7, "Funcional",
       "Para ahorrar costos, una Dirección Seccional propone atender presencialmente al público solo 20 horas a la semana.",
       "¿Es viable esta propuesta según el CPACA?",
       "C",
       ["Sí, cada seccional fija libremente su horario de atención.",
        "Sí, siempre que se publique el nuevo horario en la página web.",
        "No, porque las autoridades deben garantizar atención personal al público como mínimo 40 horas a la semana, en horarios que satisfagan las necesidades del servicio."],
       "La opción C es la correcta: el Art. 7 num. 2 del CPACA fija un mínimo de 40 horas semanales de atención personal al público. Las opciones A y B desconocen ese mínimo legal.",
       "Ley 1437 de 2011 Art. 7 num. 2"),
    _q(7, "Funcional",
       "En la campaña de renta de personas naturales, una usuaria le pide al Analista IV que le diligencie y presente la declaración usando la clave y la firma electrónica de ella, que le entrega en un papel.",
       "¿Cuál es la actuación correcta?",
       "B",
       ["Recibir la clave y presentar la declaración por ella para agilizar la fila.",
        "Guiarla paso a paso para que ella misma diligencie y firme con su IFE, explicándole cada renglón, sin usar sus credenciales.",
        "Negarle la asistencia porque la declaración es responsabilidad exclusiva del contribuyente."],
       "La opción B es la correcta: asistir no es sustituir; la declaración la presenta y firma el contribuyente con su IFE, que es personal e intransferible. La opción A expone al servidor y a la usuaria a riesgos de seguridad y de responsabilidad. La opción C desconoce la función de asistencia en las campañas.",
       "Ficha CC-AU-2010 (función esencial 5) · Resolución DIAN 000070 de 2016"),

    # ---------------------------- MÓDULO 8: HERRAMIENTAS INFORMÁTICAS ----------------------------
    _q(8, "Funcional",
       "El Analista IV tiene en la celda B1 el valor de la UVT y en la columna A, desde A3, los valores de varias sanciones en UVT. Quiere escribir en C3 una fórmula que pueda copiar hacia abajo para convertir cada valor a pesos.",
       "¿Cuál es la fórmula correcta para C3?",
       "A",
       ["=A3*$B$1",
        "=A3*B1",
        "=$A$3*B1"],
       "La opción A es la correcta: la referencia absoluta $B$1 mantiene fija la celda de la UVT al copiar, mientras A3 (relativa) cambia a A4, A5, etc. En la opción B, B1 se desplazaría a B2, B3... (celdas vacías). En la opción C, la referencia que queda fija es A3 y la que se desplaza es la de la UVT.",
       "Competencias ofimáticas — referencias relativas y absolutas en Excel"),
    _q(8, "Funcional",
       "En una hoja de Excel, la columna C (C2:C500) registra el tipo de cada PQRSF recibida. El jefe pide saber cuántas fueron quejas.",
       "¿Qué fórmula entrega el dato directamente?",
       "C",
       ["=SUMA(C2:C500)",
        "=PROMEDIO(C2:C500)",
        "=CONTAR.SI(C2:C500;\"Queja\")"],
       "La opción C es la correcta: CONTAR.SI cuenta las celdas de un rango que cumplen un criterio. SUMA y PROMEDIO operan con valores numéricos y no cuentan textos según un criterio.",
       "Competencias ofimáticas — funciones de Excel"),
    _q(8, "Funcional",
       "El Analista IV recibe en su correo institucional un mensaje con el logo de la DIAN que dice que su cuenta será bloqueada si no ingresa en 2 horas a un enlace para 'validar su contraseña'.",
       "¿Qué debe hacer?",
       "B",
       ["Ingresar al enlace y cambiar la contraseña para evitar el bloqueo.",
        "No abrir el enlace ni entregar credenciales, verificar por los canales oficiales y reportar el correo a la mesa de servicio o al área de seguridad de la información.",
        "Reenviar el correo a todos sus compañeros para que estén atentos."],
       "La opción B es la correcta: se trata de un caso típico de phishing (urgencia, enlace y solicitud de credenciales); lo indicado es no interactuar, verificar y reportar. La opción A entrega las credenciales. La opción C propaga el correo malicioso.",
       "Ley 1273 de 2009 · Política de Seguridad Digital"),
    _q(8, "Funcional",
       "El Analista IV debe levantarse unos minutos de su puesto mientras en la pantalla está abierta la información del RUT de un contribuyente.",
       "¿Cuál es la práctica correcta de seguridad de la información?",
       "A",
       ["Bloquear la sesión del equipo (por ejemplo, con Windows + L) antes de retirarse.",
        "Pedirle al ciudadano que espera que vigile el equipo.",
        "Apagar el monitor y dejar la sesión abierta."],
       "La opción A es la correcta: bloquear la sesión protege la confidencialidad de la información reservada. La opción B expone datos reservados a un tercero. La opción C deja la sesión accesible para cualquiera.",
       "Seguridad de la información (confidencialidad) · Estatuto Tributario Art. 583"),
    _q(8, "Funcional",
       "Para una campaña de actualización del RUT, el Analista IV debe enviar el mismo correo informativo a 80 contribuyentes desde el correo institucional.",
       "¿Cómo debe enviarlo para proteger los datos personales?",
       "C",
       ["Poner las 80 direcciones en el campo 'Para'.",
        "Poner las 80 direcciones en el campo 'CC'.",
        "Poner las 80 direcciones en el campo 'CCO' (copia oculta)."],
       "La opción C es la correcta: con CCO ningún destinatario ve las direcciones de los demás, lo que protege los datos personales (Ley 1581 de 2012). En las opciones A y B todos los destinatarios verían las direcciones de los demás.",
       "Ley 1581 de 2012 · Buenas prácticas de correo institucional"),
    _q(8, "Funcional",
       "Hay que enviar 200 cartas iguales a contribuyentes, cada una con el nombre, el NIT y la dirección del destinatario, que están en una hoja de Excel.",
       "¿Cuál es la herramienta más eficiente?",
       "B",
       ["Copiar y pegar cada dato manualmente en 200 documentos de Word.",
        "La función de combinar correspondencia de Word usando la hoja de Excel como origen de datos.",
        "Hacer las cartas en PowerPoint, una por diapositiva."],
       "La opción B es la correcta: la combinación de correspondencia genera documentos personalizados de forma automática a partir de una lista de datos. La opción A es lenta y propensa a errores. La opción C usa una herramienta inadecuada.",
       "Competencias ofimáticas — Word"),

    # ---------------------------- MÓDULO 9: BUEN GOBIERNO / DISCIPLINARIO ----------------------------
    _q(9, "Funcional",
       "Un servidor público le dice a un contribuyente que, si no le entrega dinero, 'perderá' su solicitud y le saldrá una sanción. El contribuyente se siente presionado y paga.",
       "¿Cómo se denomina la conducta del servidor?",
       "C",
       ["Cohecho por dar u ofrecer.",
        "Cohecho impropio.",
        "Concusión, porque el servidor, abusando del cargo, constriñó o indujo al ciudadano a dar dinero."],
       "La opción C es la correcta: la concusión (Art. 404 C.P.) se configura cuando el servidor, abusando de su cargo, constriñe o induce a alguien a dar o prometer dinero. El cohecho por dar u ofrecer (opción A) lo comete el particular. El cohecho impropio (opción B) es aceptar dinero para ejecutar un acto propio del cargo, sin constreñimiento.",
       "Código Penal Arts. 404, 406 y 407"),
    _q(9, "Funcional",
       "Al Analista IV le asignan por reparto resolver una petición presentada por una sociedad de la que fue socio hasta hace seis meses y con la que mantiene una controversia económica.",
       "¿Cómo debe proceder?",
       "A",
       ["Declararse impedido y enviar la actuación con escrito motivado a su superior dentro de los 3 días siguientes, para que este decida.",
        "Resolver la petición de forma desfavorable, para que nadie piense que favoreció a su antigua sociedad.",
        "Devolver la petición a la sociedad para que la presente en otra seccional."],
       "La opción A es la correcta: existe causal de impedimento (interés y controversia con el interesado, Art. 11 CPACA); el servidor debe enviar la actuación a su superior dentro de los 3 días siguientes (Art. 12), quien decide en 10 días. La opción B también es una decisión parcializada. La opción C traslada indebidamente la carga al peticionario.",
       "Ley 1437 de 2011 Arts. 11 y 12"),
    _q(9, "Funcional",
       "En una capacitación disciplinaria se pregunta qué sanción corresponde, según el Código General Disciplinario, a una falta gravísima cometida con dolo.",
       "¿Cuál es la respuesta correcta?",
       "B",
       ["Amonestación escrita.",
        "Destitución e inhabilidad general.",
        "Multa."],
       "La opción B es la correcta: la Ley 1952 de 2019 sanciona las faltas gravísimas dolosas o realizadas con culpa gravísima con destitución e inhabilidad general. La amonestación escrita corresponde a las faltas leves culposas y la multa a las leves dolosas.",
       "Ley 1952 de 2019 (Código General Disciplinario)"),
    _q(9, "Funcional",
       "Una servidora atiende cada trámite con prontitud, termina sus asuntos dentro de los términos, revisa con cuidado los soportes y usa con austeridad los recursos de la oficina.",
       "¿Qué valor del Código de Integridad refleja principalmente su conducta?",
       "C",
       ["Justicia.",
        "Respeto.",
        "Diligencia."],
       "La opción C es la correcta: la Diligencia consiste en cumplir los deberes con atención, prontitud, destreza y eficiencia, optimizando el uso de los recursos del Estado. La Justicia se refiere a la imparcialidad y el Respeto al trato digno.",
       "Ley 2016 de 2020 (Código de Integridad del Servicio Público)"),
    _q(9, "Funcional",
       "El Analista IV descubre que un compañero ha estado inscribiendo en el RUT a personas inexistentes para crear empresas de papel, aparentemente a cambio de dinero.",
       "¿Cuál es su deber?",
       "A",
       ["Denunciar los hechos ante la autoridad competente y ponerlos en conocimiento de Control Disciplinario Interno.",
        "Hablar con el compañero para que deje de hacerlo y no decir nada más.",
        "Esperar a tener pruebas absolutamente concluyentes antes de informar cualquier cosa."],
       "La opción A es la correcta: el servidor público tiene el deber de denunciar los delitos de los que tenga conocimiento (Ley 906 de 2004 Art. 67) y de informar las posibles faltas disciplinarias. Las opciones B y C encubren o retrasan la acción frente a hechos graves; no se exige tener la prueba completa para denunciar.",
       "Ley 906 de 2004 Art. 67 · Ley 1952 de 2019 · Ley 1474 de 2011"),

    # ---------------------------- MÓDULO 10: CPACA ----------------------------
    _q(10, "Funcional",
       "Después de notificado un acto, la Seccional advierte que el apellido del ciudadano quedó mal escrito por un error de digitación. El contenido de la decisión es correcto.",
       "¿Qué procede según el CPACA?",
       "B",
       ["Revocar el acto y volver a tramitar toda la actuación desde el inicio.",
        "Corregir el error formal en cualquier tiempo, de oficio o a petición de parte; la corrección no revive los términos para interponer recursos.",
        "Dejar el error, porque una vez notificado el acto ya no puede modificarse."],
       "La opción B es la correcta: el Art. 45 del CPACA permite corregir en cualquier tiempo los errores aritméticos, de digitación, de transcripción o de omisión de palabras, sin que se revivan los términos. La opción A es desproporcionada. La opción C desconoce esta facultad.",
       "Ley 1437 de 2011 Art. 45"),
    _q(10, "Funcional",
       "Un contribuyente quiere interponer recurso de reposición contra el auto que simplemente fija la fecha y hora de una visita de verificación de su dirección.",
       "¿Procede el recurso?",
       "C",
       ["Sí, contra todo acto administrativo proceden siempre los recursos de reposición y apelación.",
        "Sí, pero solo el de apelación.",
        "No, porque contra los actos de trámite, preparatorios o de ejecución no proceden recursos, salvo norma expresa."],
       "La opción C es la correcta: el Art. 75 del CPACA dispone que no hay recurso contra los actos de carácter general ni contra los de trámite, preparatorios o de ejecución. El auto que fija una visita es de trámite. Las opciones A y B desconocen esa improcedencia.",
       "Ley 1437 de 2011 Art. 75"),
    _q(10, "Funcional",
       "Un ciudadano presentó una petición de fondo sobre un asunto particular hace tres meses y medio y no ha recibido ninguna decisión. No se trata de una petición de documentos.",
       "¿Cuál es la situación jurídica según el CPACA?",
       "A",
       ["Se configuró el silencio administrativo negativo: se entiende negada la petición, y la autoridad sigue obligada a decidir salvo que el interesado ya haya recurrido el acto presunto o demandado.",
        "Se configuró el silencio administrativo positivo y el ciudadano obtuvo lo que pidió.",
        "La petición caducó y el ciudadano debe presentarla de nuevo."],
       "La opción A es la correcta: el Art. 83 del CPACA establece que, transcurridos 3 meses sin decisión, la petición se entiende negada, lo que no exime a la autoridad del deber de decidir. La opción B confunde la regla general con el silencio positivo, que solo opera cuando la ley lo prevé expresamente. La opción C inventa una caducidad.",
       "Ley 1437 de 2011 Arts. 83 y 84"),
    _q(10, "Funcional",
       "El funcionario que expidió un acto rechazó el recurso de apelación que el ciudadano interpuso en término y en debida forma. El ciudadano quiere que el superior revise ese rechazo.",
       "¿Qué recurso debe interponer y en qué plazo?",
       "C",
       ["Reposición, dentro de los 10 días siguientes.",
        "Revocatoria directa, en cualquier tiempo.",
        "Queja, directamente ante el superior, dentro de los 5 días siguientes a la notificación de la decisión que rechazó la apelación."],
       "La opción C es la correcta: según el Art. 74 num. 3 del CPACA, el recurso de queja procede cuando se rechaza la apelación y se interpone ante el superior dentro de los 5 días siguientes a la notificación del rechazo. Las opciones A y B no son el mecanismo previsto para controlar el rechazo de la apelación.",
       "Ley 1437 de 2011 Art. 74 num. 3"),
    _q(10, "Funcional",
       "Una petición llega sin indicar la dirección del peticionario, pero trae su correo electrónico y su teléfono y es perfectamente comprensible.",
       "¿Cómo debe actuar la autoridad conforme a los principios del CPACA?",
       "B",
       ["Rechazarla por no cumplir todos los requisitos formales del contenido mínimo.",
        "Darle trámite, removiendo los obstáculos puramente formales y usando los datos de contacto disponibles, en aplicación del principio de eficacia.",
        "Archivarla y esperar a que el ciudadano pregunte por ella."],
       "La opción B es la correcta: el principio de eficacia (Art. 3 num. 11 CPACA) obliga a remover de oficio los obstáculos puramente formales y a evitar decisiones inhibitorias. Las opciones A y C privilegian la forma sobre el derecho del ciudadano.",
       "Ley 1437 de 2011 Art. 3 num. 11"),
    _q(10, "Funcional",
       "Una resolución no se notificó en debida forma, pero el interesado presentó dentro del término un recurso de reposición contra ella, discutiendo su contenido.",
       "¿Qué efecto tiene esta actuación del interesado?",
       "A",
       ["Se entiende notificado por conducta concluyente, y el acto produce efectos desde ese momento.",
        "El recurso debe rechazarse porque el acto nunca fue notificado.",
        "La notificación irregular anula automáticamente el acto."],
       "La opción A es la correcta: el Art. 72 del CPACA establece que sin notificación en debida forma el acto no produce efectos, salvo que el interesado revele que lo conoce, consienta la decisión o interponga los recursos legales. La opción B desconoce esa regla. La opción C confunde la falta de notificación (eficacia) con la nulidad (validez).",
       "Ley 1437 de 2011 Art. 72"),
    _q(10, "Funcional",
       "Un contribuyente fue notificado de una liquidación oficial de revisión del impuesto sobre la renta expedida por la DIAN y quiere controvertirla en sede administrativa.",
       "¿Qué recurso procede y en qué plazo?",
       "B",
       ["Reposición, dentro de los 10 días siguientes, conforme al CPACA.",
        "Reconsideración, dentro de los 2 meses siguientes a la notificación, conforme al Art. 720 del Estatuto Tributario.",
        "Apelación ante el Ministerio de Hacienda, dentro de los 5 días siguientes."],
       "La opción B es la correcta: contra las liquidaciones oficiales y las resoluciones que imponen sanciones tributarias procede el recurso de reconsideración dentro de los 2 meses siguientes a su notificación (Art. 720 E.T.). El procedimiento tributario es especial y prevalece; el CPACA solo se aplica de forma supletiva (Art. 34 CPACA). Las opciones A y C aplican reglas que no corresponden.",
       "Estatuto Tributario Art. 720 · Ley 1437 de 2011 Art. 34"),
    _q(10, "Funcional",
       "Un acto administrativo particular quedó en firme hace seis años y la administración nunca adelantó ninguna actuación para ejecutarlo.",
       "Según el CPACA, ¿qué ocurrió con el acto?",
       "C",
       ["Sigue siendo plenamente ejecutable, porque los actos en firme no pierden fuerza.",
        "Fue anulado de pleno derecho por el paso del tiempo.",
        "Perdió su fuerza ejecutoria, porque al cabo de 5 años de estar en firme la autoridad no realizó los actos para ejecutarlo."],
       "La opción C es la correcta: el Art. 91 num. 3 del CPACA prevé la pérdida de ejecutoriedad cuando, al cabo de 5 años de estar en firme, la autoridad no ha realizado los actos que le correspondan para ejecutarlo. La opción A desconoce esta causal. La opción B confunde la pérdida de ejecutoriedad con la nulidad, que solo declara la jurisdicción.",
       "Ley 1437 de 2011 Art. 91 num. 3"),

    # ---------------------------- MÓDULO 11: CONSTITUCIÓN ----------------------------
    _q(11, "Funcional",
       "Un ciudadano le cuenta al Analista IV que hace cinco meses presentó una petición ante otra entidad y nunca le respondieron. Pregunta qué mecanismo constitucional puede usar para que lo protejan.",
       "¿Qué orientación es correcta?",
       "A",
       ["La acción de tutela, porque el derecho de petición es un derecho fundamental; el juez debe decidir en un plazo máximo de 10 días.",
        "La acción popular, porque protege los derechos de petición individuales.",
        "El habeas corpus, porque se le está negando un derecho."],
       "La opción A es la correcta: el derecho de petición (Art. 23 C.P.) es fundamental y la tutela (Art. 86 C.P.) es el mecanismo para su protección inmediata; el fallo debe proferirse en no más de 10 días. La acción popular protege derechos colectivos y el habeas corpus protege la libertad personal.",
       "Constitución Política Arts. 23 y 86 · Decreto 2591 de 1991"),
    _q(11, "Funcional",
       "Un usuario afirma en ventanilla que 'la DIAN se inventó por resolución un nuevo impuesto' y que eso le parece arbitrario.",
       "¿Qué principio constitucional debe explicarle el Analista IV?",
       "C",
       ["Que la DIAN puede crear impuestos nacionales mediante resolución cuando lo autoriza el Ministerio de Hacienda.",
        "Que el Presidente de la República puede crear impuestos por decreto en cualquier momento.",
        "Que, en tiempo de paz, solamente el Congreso, las asambleas departamentales y los concejos pueden imponer contribuciones; la DIAN administra los tributos, pero no los crea."],
       "La opción C es la correcta: el Art. 338 de la Constitución consagra el principio de legalidad tributaria. La DIAN administra y controla los impuestos que crea la ley. Las opciones A y B desconocen ese principio.",
       "Constitución Política Arts. 150 num. 12 y 338"),
    _q(11, "Funcional",
       "Un servidor justifica no haber tramitado una petición diciendo que 'solo responde por lo que hace, no por lo que deja de hacer'.",
       "Según el Art. 6 de la Constitución, ¿es correcta su afirmación?",
       "B",
       ["Sí, los servidores públicos solo responden por las acciones que infringen la ley.",
        "No: los servidores públicos responden por infringir la Constitución y las leyes y también por omisión o extralimitación en el ejercicio de sus funciones.",
        "Sí, la responsabilidad por omisión solo se aplica a los particulares."],
       "La opción B es la correcta: el Art. 6 C.P. establece que los particulares responden por infringir la Constitución y las leyes, y los servidores públicos por la misma causa y por omisión o extralimitación de sus funciones. Las opciones A y C invierten la regla.",
       "Constitución Política Art. 6"),
    _q(11, "Funcional",
       "Un ciudadano quiere informar sobre un posible manejo indebido de recursos públicos que causó un detrimento al patrimonio del Estado en una entidad territorial.",
       "¿Qué órgano ejerce el control fiscal?",
       "A",
       ["La Contraloría General de la República (y las contralorías territoriales).",
        "La Procuraduría General de la Nación.",
        "La Registraduría Nacional del Estado Civil."],
       "La opción A es la correcta: la Contraloría ejerce el control fiscal (Arts. 117 y 267 C.P.). La Procuraduría ejerce principalmente el control disciplinario y la Registraduría hace parte de la organización electoral.",
       "Constitución Política Arts. 117, 120 y 267"),
    _q(11, "Funcional",
       "Un compañero de concurso pregunta por qué el ingreso a la DIAN se hace mediante una prueba de la CNSC y no por designación directa.",
       "¿Cuál es el fundamento constitucional?",
       "C",
       ["Que la DIAN decide libremente si convoca o no concursos.",
        "Que todos los empleos públicos son de libre nombramiento y remoción.",
        "Que los empleos del Estado son, por regla general, de carrera, y el ingreso se hace por méritos mediante concurso; la CNSC administra y vigila las carreras."],
       "La opción C es la correcta: los Arts. 125 y 130 de la Constitución establecen la carrera administrativa basada en el mérito y asignan a la CNSC su administración y vigilancia. La DIAN tiene un sistema específico de carrera (Decreto Ley 071 de 2020). Las opciones A y B contradicen la regla constitucional.",
       "Constitución Política Arts. 125 y 130 · Decreto Ley 071 de 2020"),
    _q(11, "Funcional",
       "Un usuario descubre que en el RUT figura una dirección antigua suya y pregunta qué derecho tiene sobre esa información.",
       "¿Cuál es la orientación correcta?",
       "B",
       ["Ninguno: la información del RUT es de la DIAN y solo ella decide si la modifica.",
        "Tiene derecho a conocer, actualizar y rectificar sus datos (Art. 15 C.P.); debe actualizar su RUT por los canales dispuestos, lo cual además es su obligación legal.",
        "Debe interponer una acción de tutela para que se corrija la dirección."],
       "La opción B es la correcta: el habeas data (Art. 15 C.P.) le da derecho a conocer, actualizar y rectificar sus datos, y la actualización del RUT es además una obligación del inscrito. La opción A desconoce el derecho. La opción C es improcedente porque existe un mecanismo ordinario y expedito.",
       "Constitución Política Art. 15 · Ley 1581 de 2012 · E.T. Art. 658-3"),

    # ---------------------------- MÓDULO 12: CULTURA DE LA CONTRIBUCIÓN ----------------------------
    _q(12, "Funcional",
       "En una charla en un colegio, un estudiante pregunta: '¿Para qué pagamos impuestos si el Estado no me da nada a mí directamente?'.",
       "¿Cuál es la respuesta más acorde con la cultura de la contribución?",
       "A",
       ["Explicar que contribuir es un deber constitucional (Art. 95 num. 9) y que los impuestos financian bienes y servicios colectivos, como salud, educación y vías, no contraprestaciones individuales.",
        "Explicarle que los impuestos son una sanción por tener ingresos.",
        "Decirle que si no recibe un beneficio directo, no está obligado a pagar."],
       "La opción A es la correcta: la cultura de la contribución se basa en entender el deber constitucional de contribuir y el destino colectivo de los tributos. La opción B transmite una idea errónea y negativa. La opción C es jurídicamente falsa.",
       "Constitución Política Art. 95 num. 9"),
    _q(12, "Funcional",
       "Al final de un programa de talleres sobre RUT y factura electrónica para emprendedores, el jefe pide al Analista IV evaluar el programa.",
       "¿Cuál es la forma más completa de evaluarlo?",
       "C",
       ["Contar cuántos folletos se entregaron.",
        "Preguntar a los talleristas si les pareció que salió bien.",
        "Medir indicadores de cobertura frente a la meta, de aprendizaje (prueba de entrada y salida), de satisfacción y de resultado, por ejemplo cuántos asistentes se inscribieron o facturaron correctamente."],
       "La opción C es la correcta: evaluar un programa pedagógico (función esencial 6) requiere indicadores de cobertura, aprendizaje, satisfacción y resultado o impacto en el cumplimiento. Las opciones A y B miden actividades u opiniones, no resultados.",
       "Ficha CC-AU-2010 (función esencial 6) · ciclo PHVA"),
    _q(12, "Funcional",
       "Un emprendedor pregunta cuánto cobran los Núcleos de Apoyo Contable y Fiscal (NAF) por orientarlo en la inscripción en el RUT y la facturación.",
       "¿Qué debe responder el Analista IV?",
       "B",
       ["Que cobran una tarifa fijada por la DIAN según los ingresos del usuario.",
        "Que los NAF son un programa de la DIAN con universidades en el que estudiantes formados brindan orientación gratuita a personas naturales y pequeños negocios.",
        "Que los NAF solo atienden a grandes contribuyentes."],
       "La opción B es la correcta: los NAF son una estrategia de la DIAN con instituciones de educación superior para brindar orientación tributaria gratuita, principalmente a personas naturales, emprendedores y pequeñas empresas. Las opciones A y C describen mal el programa.",
       "Programa NAF — DIAN"),
    _q(12, "Funcional",
       "El jefe le pide al Analista IV lanzar en un mes un nuevo programa pedagógico sobre la declaración de renta en Tuluá.",
       "¿Cuál debe ser el primer paso?",
       "A",
       ["Hacer un diagnóstico de las necesidades y del público objetivo y definir objetivos de aprendizaje medibles (fase de planear).",
        "Imprimir material y repartirlo en la plaza principal.",
        "Programar de inmediato charlas magistrales con el texto completo del Estatuto Tributario."],
       "La opción A es la correcta: el ciclo PHVA empieza por planear, con un diagnóstico y objetivos medibles que luego permitan evaluar. Las opciones B y C ejecutan actividades sin diagnóstico ni objetivos, por lo que no podrán evaluarse.",
       "Ficha CC-AU-2010 (función esencial 6) · ciclo PHVA"),
]

# =============================================================================
# FLASHCARDS AMPLIADAS
# =============================================================================
EXTRA_FLASHCARDS = [
    (1, "¿Qué es el RUT según el Art. 555-2 E.T.?", "El mecanismo único para identificar, ubicar y clasificar a los sujetos de obligaciones administradas y controladas por la DIAN.", "E.T. Art. 555-2", "Conceptos Fiscales"),
    (1, "¿Cuándo debe inscribirse en el RUT quien va a iniciar una actividad?", "Antes de iniciar la actividad. La inscripción posterior es extemporánea y sancionable.", "E.T. Arts. 555-2 y 658-3", "Plazos Legales"),
    (1, "Formulario del RUT", "Formulario 001.", "DIAN", "Canales DIAN"),
    (2, "Petición incompleta: ¿en cuánto tiempo se requiere al ciudadano?", "Dentro de los 10 días siguientes a la radicación; el ciudadano tiene 1 mes (prorrogable) para completar. Si no lo hace, desistimiento tácito.", "Ley 1755 de 2015 Art. 17", "Plazos Legales"),
    (2, "Ampliación del término para responder una petición", "Informar antes del vencimiento los motivos y el nuevo plazo, que no puede exceder el doble del inicial.", "Ley 1755 de 2015 Art. 14 par.", "Plazos Legales"),
    (2, "Petición oscura (no se entiende su finalidad)", "Se devuelve al interesado para que la corrija o aclare dentro de los 10 días siguientes; si no lo hace, se archiva.", "Ley 1755 de 2015 Art. 19", "Plazos Legales"),
    (2, "Recurso de insistencia (información reservada)", "Si el peticionario insiste, el juez o tribunal administrativo decide en 10 días.", "Ley 1755 de 2015 Art. 26", "Plazos Legales"),
    (2, "¿Los 'días' de la Ley 1755 son hábiles o calendario?", "Hábiles. Los plazos en meses y años se cuentan según el calendario.", "Ley 4 de 1913 Art. 62", "Plazos Legales"),
    (2, "Características de una respuesta válida a una petición", "De fondo, clara, precisa, congruente con lo pedido, oportuna y puesta en conocimiento del peticionario (puede ser negativa si es motivada).", "Jurisprudencia Corte Constitucional", "Normativa"),
    (3, "Topes para declarar renta (persona natural)", "Patrimonio bruto > 4.500 UVT; ingresos brutos ≥ 1.400 UVT; consumos con tarjeta, compras o consignaciones > 1.400 UVT; o ser responsable de IVA.", "E.T. Arts. 592-594-3", "Conceptos Fiscales"),
    (3, "Tope de ingresos para ser NO responsable de IVA", "Ingresos brutos inferiores a 3.500 UVT, entre otras condiciones (un solo establecimiento, no usuario aduanero, sin franquicias, etc.).", "E.T. Art. 437 par. 3", "Conceptos Fiscales"),
    (3, "Bien exento vs. bien excluido de IVA", "Exento: tarifa 0 % con derecho a devolución. Excluido: no causa IVA y no da derecho a devolución.", "E.T. Arts. 420, 424 y 477", "Conceptos Fiscales"),
    (3, "Residencia fiscal de personas naturales", "Permanecer en Colombia más de 183 días calendario (continuos o no) en un periodo de 365 días.", "E.T. Art. 10", "Conceptos Fiscales"),
    (3, "Tope de ingresos del Régimen SIMPLE", "Ingresos brutos inferiores a 100.000 UVT.", "E.T. Art. 905", "Conceptos Fiscales"),
    (3, "Viajeros con efectivo", "Más de USD 10.000 (o su equivalente) en efectivo se declara en la declaración de equipaje.", "Decreto 1165 de 2019", "Aduanero"),
    (3, "¿Quién controla el régimen cambiario de importaciones y exportaciones?", "La DIAN (comercio exterior de bienes y servicios y profesionales del cambio). La Superintendencia de Sociedades controla la inversión internacional y el endeudamiento externo.", "Decreto Ley 2245 de 2011", "Cambiario"),
    (3, "Contrabando técnico", "La mercancía se presenta a la aduana pero con información falsa (subfacturación, origen o clasificación falsos) para pagar menos tributos.", "C.P. Art. 321 · Ley 1762 de 2015", "Conceptos Fiscales"),
    (3, "Recurso contra liquidaciones oficiales y sanciones tributarias", "Recurso de reconsideración, dentro de los 2 meses siguientes a la notificación.", "E.T. Art. 720", "Plazos Legales"),
    (3, "Corte normativo de la Guía DIAN 2676", "Solo se evalúan normas vigentes expedidas ANTES del 19 de junio de 2026 (la Ley 2586 de 2026 queda por fuera).", "Guía de Orientación al Aspirante", "Normativa"),
    (4, "Horario mínimo de atención personal al público", "40 horas a la semana, en horarios que satisfagan las necesidades del servicio.", "CPACA Art. 7 num. 2", "Servicio al Usuario"),
    (4, "Carta de Trato Digno", "Documento que la entidad debe expedir y hacer visible, con los derechos de los usuarios y los medios para garantizarlos.", "CPACA Art. 7 num. 5", "Servicio al Usuario"),
    (4, "Centro de Relevo", "Servicio del Estado que permite la comunicación de las personas sordas mediante intérprete de lengua de señas.", "Ley 1618 de 2013 (ajustes razonables)", "Servicio al Usuario"),
    (4, "Indicadores para administrar canales", "Tiempo de espera, tiempo de atención, nivel de servicio, tasa de abandono, resolución en primer contacto y satisfacción.", "Política de Servicio al Ciudadano", "Canales DIAN"),
    (5, "Tiempo máximo de la reserva de información pública reservada", "15 años.", "Ley 1712 de 2014 Art. 22", "Plazos Legales"),
    (5, "Información clasificada vs. reservada", "Clasificada: protege derechos de personas (intimidad, secretos comerciales), Art. 18. Reservada: protege intereses públicos (defensa, seguridad, relaciones internacionales), Art. 19.", "Ley 1712 de 2014", "Normativa"),
    (5, "Datos personales: términos para consultas y reclamos", "Consulta: 10 días hábiles (+5). Reclamo: 15 días hábiles (+8).", "Ley 1581 de 2012 Arts. 14 y 15", "Plazos Legales"),
    (5, "Líneas de defensa del MIPG", "Estratégica (alta dirección), 1.ª (líderes de proceso: controles diarios), 2.ª (planeación/riesgos: monitoreo), 3.ª (Control Interno: evaluación independiente).", "Decreto 1499 de 2017", "MIPG"),
    (5, "Componentes del MECI", "Ambiente de control, evaluación del riesgo, actividades de control, información y comunicación, actividades de monitoreo.", "Manual Operativo MIPG", "MIPG"),
    (5, "Las 7 dimensiones del MIPG", "1 Talento Humano · 2 Direccionamiento Estratégico y Planeación · 3 Gestión con Valores para Resultados · 4 Evaluación de Resultados · 5 Información y Comunicación · 6 Gestión del Conocimiento y la Innovación · 7 Control Interno.", "Decreto 1499 de 2017", "MIPG"),
    (5, "Transferencia primaria vs. secundaria", "Primaria: archivo de gestión → archivo central. Secundaria: archivo central → archivo histórico.", "Ley 594 de 2000", "Gestión Documental"),
    (5, "TRD vs. TVD", "TRD: tiempos de retención de la documentación producida. TVD: valoración de fondos acumulados (documentos anteriores a la TRD).", "Ley 594 de 2000 · Acuerdo AGN 001 de 2024", "Gestión Documental"),
    (5, "Radicación de comunicaciones oficiales", "En la ventanilla única de correspondencia, con número consecutivo, fecha y hora.", "Acuerdo AGN 060 de 2001", "Gestión Documental"),
    (6, "Formato de las pruebas Comportamental e Integridad (DIAN 2676)", "Escala Likert de 4 opciones con 2 subescalas de control de respuestas exageradamente favorables. Responde con consistencia y realismo.", "Guía de Orientación al Aspirante", "Competencias"),
    (7, "CONPES 3785 de 2013", "Política de Eficiencia Administrativa al Servicio del Ciudadano: ventanilla hacia adentro (arreglos internos) y ventanilla hacia afuera (canales, certidumbre, expectativas).", "CONPES 3785 de 2013", "Servicio al Usuario"),
    (7, "Prohibición de exigir documentos que reposan en la entidad", "La autoridad no puede pedir al ciudadano documentos o información que ya tiene; debe consultarlos.", "CPACA Art. 9 · Decreto Ley 019 de 2012 Art. 9", "Servicio al Usuario"),
    (7, "Dependencia de quejas, sugerencias y reclamos", "Toda entidad pública debe tener al menos una dependencia encargada de recibirlas, tramitarlas y resolverlas.", "Ley 1474 de 2011 Art. 76", "Servicio al Usuario"),
    (7, "Atributos del buen servicio", "Respetuoso, amable, confiable, empático, incluyente, oportuno y efectivo.", "Protocolos de Servicio al Ciudadano", "Servicio al Usuario"),
    (8, "Referencia absoluta en Excel", "$A$1: no cambia al copiar la fórmula. $A1 fija la columna; A$1 fija la fila.", "Excel", "Herramientas"),
    (8, "Contar celdas que cumplen un criterio", "=CONTAR.SI(rango;criterio). Para sumar según un criterio: =SUMAR.SI(rango;criterio;rango_suma).", "Excel", "Herramientas"),
    (8, "CC vs. CCO", "CC: copia visible para todos. CCO: copia oculta (protege las direcciones en los envíos masivos).", "Correo electrónico", "Herramientas"),
    (8, "Ley de delitos informáticos", "Ley 1273 de 2009: acceso abusivo a sistema informático (269A), violación de datos personales (269F), suplantación de sitios web (269G), hurto por medios informáticos (269I).", "Ley 1273 de 2009", "Herramientas"),
    (8, "Triada de la seguridad de la información", "Confidencialidad, integridad y disponibilidad.", "MSPI — MinTIC", "Herramientas"),
    (8, "Valor jurídico del mensaje de datos y la firma digital", "Ley 527 de 1999 (equivalencia funcional).", "Ley 527 de 1999", "Herramientas"),
    (9, "Ley que adopta el Código de Integridad del Servicio Público", "Ley 2016 de 2020. Valores: Honestidad, Respeto, Compromiso, Diligencia y Justicia.", "Ley 2016 de 2020", "Integridad"),
    (9, "Concusión vs. cohecho propio vs. cohecho impropio", "Concusión: el servidor constriñe o induce a dar dinero. Cohecho propio: recibe dinero para omitir o retardar un acto o hacer uno contrario a sus deberes. Cohecho impropio: acepta dinero por un acto propio de su cargo.", "C.P. Arts. 404-406", "Integridad"),
    (9, "Trámite del impedimento", "El servidor envía la actuación a su superior dentro de los 3 días siguientes; el superior decide en 10 días.", "CPACA Art. 12", "Plazos Legales"),
    (9, "Parentesco que genera impedimento", "Hasta el 4.º grado de consanguinidad (primos), 2.º de afinidad (suegros, cuñados) o 1.º civil.", "CPACA Art. 11", "Integridad"),
    (9, "Sanción para una falta gravísima dolosa", "Destitución e inhabilidad general.", "Ley 1952 de 2019", "Integridad"),
    (10, "Los 13 principios del CPACA", "Debido proceso, igualdad, imparcialidad, buena fe, moralidad, participación, responsabilidad, transparencia, publicidad, coordinación, eficacia, economía y celeridad.", "CPACA Art. 3", "Normativa"),
    (10, "Los 7 principios del Art. 209 C.P.", "Igualdad, moralidad, eficacia, economía, celeridad, imparcialidad y publicidad.", "Constitución Art. 209", "Normativa"),
    (10, "Corrección de errores formales", "En cualquier tiempo, de oficio o a petición de parte; no revive los términos para recursos.", "CPACA Art. 45", "Normativa"),
    (10, "Actos que no tienen recursos", "Los de carácter general y los de trámite, preparatorios o de ejecución (salvo norma expresa).", "CPACA Art. 75", "Normativa"),
    (10, "Plazo del recurso de queja", "5 días siguientes a la notificación de la decisión que rechazó la apelación.", "CPACA Art. 74 num. 3", "Plazos Legales"),
    (10, "Silencio administrativo negativo", "3 meses sin decisión sobre una petición → se entiende negada.", "CPACA Art. 83", "Plazos Legales"),
    (10, "Silencio en los recursos", "2 meses sin decidir la reposición o la apelación → decisión negativa.", "CPACA Art. 86", "Plazos Legales"),
    (10, "Notificación por aviso", "Si no se logra la notificación personal 5 días después de enviada la citación. Queda surtida al finalizar el día siguiente a la entrega del aviso.", "CPACA Arts. 68 y 69", "Plazos Legales"),
    (10, "Pérdida de ejecutoriedad por el paso del tiempo", "Cuando, al cabo de 5 años de estar en firme el acto, la autoridad no ha realizado los actos para ejecutarlo.", "CPACA Art. 91 num. 3", "Plazos Legales"),
    (10, "Notificación por conducta concluyente", "El interesado revela que conoce el acto, consiente la decisión o interpone recursos: se entiende notificado.", "CPACA Art. 72", "Normativa"),
    (11, "Art. 1 de la Constitución", "Estado social de derecho; república unitaria, descentralizada, con autonomía territorial, democrática, participativa y pluralista.", "Constitución Art. 1", "Constitución"),
    (11, "Acción de tutela", "Protege derechos fundamentales; el juez decide en máximo 10 días; es subsidiaria (salvo perjuicio irremediable).", "Constitución Art. 86 · Decreto 2591 de 1991", "Constitución"),
    (11, "Principio de legalidad tributaria", "En tiempo de paz, solo el Congreso, las asambleas y los concejos imponen contribuciones.", "Constitución Art. 338", "Constitución"),
    (11, "Principios del sistema tributario", "Equidad, eficiencia y progresividad; las leyes tributarias no son retroactivas.", "Constitución Art. 363", "Constitución"),
    (11, "Órganos de control", "Ministerio Público (Procuraduría, Defensoría, personerías) y Contraloría General de la República.", "Constitución Art. 117", "Constitución"),
    (11, "Responsabilidad de los servidores públicos", "Responden por infringir la Constitución y las leyes y por omisión o extralimitación en sus funciones.", "Constitución Art. 6", "Constitución"),
    (12, "Deber constitucional de contribuir", "Contribuir al financiamiento de los gastos e inversiones del Estado dentro de conceptos de justicia y equidad.", "Constitución Art. 95 num. 9", "Cultura de la Contribución"),
    (12, "NAF", "Núcleos de Apoyo Contable y Fiscal: DIAN + universidades; orientación tributaria gratuita a personas naturales y pequeños negocios.", "Programa NAF — DIAN", "Cultura de la Contribución"),
    (12, "Modelo de cumplimiento tributario", "Educar, facilitar, persuadir y controlar, según el comportamiento del contribuyente.", "Cultura de la contribución", "Cultura de la Contribución"),
]

EXTRA_DOCUMENTS = [
    ("Constitución Política de Colombia de 1991", "Constitución",
     "Texto vigente de la Carta Política. Para el eje 12: Arts. 1-10 (principios), 11-41 (derechos fundamentales), 86-88 (acciones), 113-131 (estructura y servidores), 209, 338 y 363.",
     "https://normograma.dian.gov.co/dian/compilacion/docs/constitucion_politica_1991.htm", "Portal Web oficial"),
    ("Normograma DIAN", "Tributario",
     "Compilación oficial de normas, doctrina y jurisprudencia de la DIAN: Estatuto Tributario actualizado, DUR 1625 de 2016, Decreto 1165 de 2019 y resoluciones.",
     "https://normograma.dian.gov.co/dian/", "Portal Web oficial"),
    ("Ley 1474 de 2011 — Estatuto Anticorrupción", "Integridad",
     "Medidas para prevenir y sancionar la corrupción. Art. 73 (Plan Anticorrupción y de Atención al Ciudadano) y Art. 76 (oficina de quejas, sugerencias y reclamos).",
     "https://normograma.dian.gov.co/dian/compilacion/docs/ley_1474_2011.htm", "Portal Web oficial"),
    ("Ley 1952 de 2019 — Código General Disciplinario", "Integridad",
     "Faltas disciplinarias (gravísimas, graves y leves), sanciones, deberes y prohibiciones de los servidores públicos.",
     "https://normograma.dian.gov.co/dian/compilacion/docs/ley_1952_2019.htm", "Portal Web oficial"),
    ("Ley 2016 de 2020 — Código de Integridad del Servicio Público", "Integridad",
     "Adopta con carácter obligatorio el Código de Integridad: Honestidad, Respeto, Compromiso, Diligencia y Justicia.",
     "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=107254", "Portal Web oficial"),
    ("Ley 1581 de 2012 — Protección de Datos Personales", "Transparencia",
     "Régimen general de habeas data: principios, derechos del titular, consultas (10 días) y reclamos (15 días).",
     "https://normograma.dian.gov.co/dian/compilacion/docs/ley_1581_2012.htm", "Portal Web oficial"),
    ("Ley 1273 de 2009 — Delitos Informáticos", "Herramientas Informáticas",
     "Protección de la información y de los datos: acceso abusivo, violación de datos personales y suplantación de sitios web.",
     "https://normograma.dian.gov.co/dian/compilacion/docs/ley_1273_2009.htm", "Portal Web oficial"),
    ("Modelo Integrado de Planeación y Gestión — MIPG (Función Pública)", "MIPG",
     "Portal oficial del MIPG con el Manual Operativo, las dimensiones, las políticas y el esquema de líneas de defensa.",
     "https://www.funcionpublica.gov.co/web/mipg", "Portal Web oficial"),
    ("Decreto 1499 de 2017 — Modelo Integrado de Planeación y Gestión", "MIPG",
     "Decreto que actualiza el MIPG (modifica el Decreto 1083 de 2015): dimensiones, políticas de gestión y desempeño, y sistema de control interno.",
     "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=83433", "Portal Web oficial"),
    ("Decreto 1165 de 2019 — Régimen de Aduanas", "Tributario",
     "Régimen aduanero vigente: importación, exportación, tránsito, declarantes y régimen de viajeros.",
     "https://normograma.dian.gov.co/dian/compilacion/docs/decreto_1165_2019.htm", "Portal Web oficial"),
    ("SIMO — Ficha del empleo y ejes temáticos (CNSC)", "CNSC",
     "Consulta en SIMO la OPEC 236799, tu citación (lugar y hora) y los ejes temáticos de tu empleo.",
     "https://simo.cnsc.gov.co/", "Portal Web oficial"),
]


# =============================================================================
# SIEMBRA
# =============================================================================
def seed_extended_content(db: Session) -> None:
    """Agrega módulos 7-12, temas, preguntas, flashcards y documentos ampliados.
    Idempotente: si los módulos nuevos ya existen, no hace nada."""
    modules = {m.number: m for m in db.query(Module).all()}
    if all(nm["number"] in modules for nm in NEW_MODULES):
        return

    # 1. Módulos nuevos con sus temas
    for nm in NEW_MODULES:
        if nm["number"] in modules:
            continue
        m = Module(
            number=nm["number"], title=nm["title"], subtitle=nm["subtitle"],
            category=nm["category"], priority=nm["priority"], icon=nm["icon"],
            description=nm["description"],
        )
        db.add(m)
        db.flush()
        for order, (title, basis, content) in enumerate(nm["topics"], start=1):
            db.add(Topic(module_id=m.id, title=title, order=order, legal_basis=basis, content=content))
        modules[nm["number"]] = m

    # 2. Temas adicionales para los módulos base
    for number, topics in EXTRA_TOPICS.items():
        m = modules.get(number)
        if not m:
            continue
        next_order = max([t.order for t in m.topics] or [0]) + 1
        for i, (title, basis, content) in enumerate(topics):
            db.add(Topic(module_id=m.id, title=title, order=next_order + i, legal_basis=basis, content=content))

    # 3. Preguntas
    for qd in EXTRA_QUESTIONS:
        m = modules.get(qd["module"])
        if not m:
            continue
        q = Question(
            module_id=m.id, category=qd["category"], case_study=qd["case_study"],
            question_text=qd["question_text"], explanation=qd["explanation"],
            legal_reference=qd["legal_reference"],
        )
        db.add(q)
        db.flush()
        for letter, text in zip(("A", "B", "C"), qd["options"]):
            db.add(Option(question_id=q.id, letter=letter, text=text, is_correct=(letter == qd["correct"])))

    # 4. Flashcards
    for number, term, definition, norm, cat in EXTRA_FLASHCARDS:
        m = modules.get(number)
        if m:
            db.add(Flashcard(module_id=m.id, term=term, definition=definition, legal_norm=norm, category=cat))

    # 5. Documentos
    existing_urls = {d.external_url for d in db.query(DocumentResource).all()}
    for title, cat, desc, url, ftype in EXTRA_DOCUMENTS:
        if url not in existing_urls:
            db.add(DocumentResource(title=title, category=cat, description=desc, external_url=url, file_type=ftype))

    db.commit()
