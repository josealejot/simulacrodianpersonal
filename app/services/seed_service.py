from sqlalchemy.orm import Session
from app.models.models import Module, Topic, Question, Option, Flashcard, DocumentResource, AppMeta
from app.services.content_opec import CONTENT_VERSION, seed_extended_content

class SeedService:
    @staticmethod
    def seed_documents(db: Session, force_reset: bool = False):
        if force_reset:
            db.query(DocumentResource).delete()
            db.commit()

        if db.query(DocumentResource).count() > 0:
            return

        documents_data = [
            {
                "title": "Decreto 1625 de 2016 - Único Reglamentario en Materia Tributaria",
                "category": "Tributario",
                "description": "Decreto Único Reglamentario del sector tributario en Colombia. Contiene la reglamentación integral del Registro Único Tributario - RUT (Arts. 1.6.1.2.1 al 1.6.1.2.29), sujetos obligados, formalización, actualización en plazo perentorio de 1 mes, causales de suspensión y cancelación definitiva.",
                "external_url": "https://normograma.dian.gov.co/dian/compilacion/docs/decreto_1625_2016.htm",
                "file_type": "Portal Web oficial"
            },
            {
                "title": "Ley 1437 de 2011 - Código de Procedimiento Administrativo y de lo Contencioso Administrativo (CPACA)",
                "category": "Procedimiento Administrativo",
                "description": "Marco legal rector de la actuación administrativa estatal. Regula los principios fundamentales (Título I), el derecho de petición (Título II), régimen de notificaciones (personal, electrónica, por aviso) y los recursos de reposición, apelación y queja en término de 10 días (Título III).",
                "external_url": "https://normograma.dian.gov.co/dian/compilacion/docs/ley_1437_2011.htm",
                "file_type": "Portal Web oficial"
            },
            {
                "title": "Ley 1755 de 2015 - Regulación Fundamental del Derecho de Petición",
                "category": "Procedimiento Administrativo",
                "description": "Ley Estatutaria que sustituyó el Título II del CPACA. Fija términos perentorios legales: 15 días petición general, 10 días solicitud de documentos/copias con aceptación tácita a los 3 días si no se responde, 30 días consultas y 5 días para traslado por competencia.",
                "external_url": "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=65334",
                "file_type": "Portal Web oficial"
            },
            {
                "title": "Estatuto Tributario Nacional (Decreto 624 de 1989) - Arts. 555-2 y 583",
                "category": "Tributario",
                "description": "Norma tributaria superior en Colombia. El Art. 555-2 consagra la obligación y administración del RUT, y el Art. 583 instituye la reserva tributaria estricta que ampara la confidencialidad de las declaraciones de renta e información privada de los contribuyentes.",
                "external_url": "https://normograma.dian.gov.co/dian/compilacion/docs/estatuto_tributario.htm",
                "file_type": "Portal Web oficial"
            },
            {
                "title": "Ley 1712 de 2014 - Transparencia y Acceso a la Información Pública",
                "category": "Transparencia",
                "description": "Ley Estatutaria de Transparencia y del Derecho de Acceso a la Información Pública Nacional. Establece el principio de máxima publicidad y delimita las excepciones taxativas de información pública clasificada y reservada.",
                "external_url": "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=56882",
                "file_type": "Portal Web oficial"
            },
            {
                "title": "Ley 594 de 2000 - Ley General de Archivos y Gestión Documental",
                "category": "Gestión Documental",
                "description": "Regula la gestión documental en las entidades del Estado. Define el ciclo vital del documento (archivo de gestión, archivo central y archivo histórico), los principios archivísticos y la obligatoriedad de las Tablas de Retención Documental (TRD).",
                "external_url": "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=4275",
                "file_type": "Portal Web oficial"
            },
            {
                "title": "Guía de Orientación al Aspirante CNSC - Convocatoria DIAN 2676",
                "category": "CNSC",
                "description": "Documento técnico y pedagógico oficial expedido por la Comisión Nacional del Servicio Civil (CNSC) para la Convocatoria DIAN 2676. Detalla la metodología de juicio situacional con 3 opciones (A, B, C) y los pesos porcentuales de las pruebas.",
                "external_url": "https://www.cnsc.gov.co/convocatorias/dian-2676",
                "file_type": "PDF Oficial"
            }
        ]

        for doc in documents_data:
            dr = DocumentResource(
                title=doc["title"],
                category=doc["category"],
                description=doc["description"],
                external_url=doc["external_url"],
                file_type=doc["file_type"]
            )
            db.add(dr)
        db.commit()

    @staticmethod
    def get_content_version(db: Session):
        meta = db.query(AppMeta).filter(AppMeta.key == "content_version").first()
        return meta.value if meta else None

    @staticmethod
    def set_content_version(db: Session, version: str):
        meta = db.query(AppMeta).filter(AppMeta.key == "content_version").first()
        if meta:
            meta.value = version
        else:
            db.add(AppMeta(key="content_version", value=version))
        db.commit()

    @staticmethod
    def seed_database(db: Session, force_reset: bool = False):
        # Si la BD tiene contenido de una versión anterior, se re-siembra SOLO el
        # contenido de estudio. El historial (exam_attempts) nunca se borra.
        if (not force_reset
                and db.query(Module).count() > 0
                and SeedService.get_content_version(db) != CONTENT_VERSION):
            force_reset = True

        SeedService.seed_documents(db, force_reset=force_reset)

        if not force_reset and db.query(Module).count() > 0:
            return  # Already seeded

        if force_reset:
            db.query(Option).delete()
            db.query(Question).delete()
            db.query(Topic).delete()
            db.query(Flashcard).delete()
            db.query(Module).delete()
            db.commit()

        # =========================================================================
        # MÓDULO 1: REGISTRO ÚNICO TRIBUTARIO - RUT (Funcional - Prioridad Máxima)
        # =========================================================================
        m1 = Module(
            number=1,
            title="Registro Único Tributario (RUT)",
            subtitle="Estatuto Tributario Art. 555-2 y Decreto 1625 de 2016 (Arts. 1.6.1.2.1 al 1.6.1.2.29)",
            category="Funcional",
            priority="Máxima",
            icon="identification",
            description="Módulo de máxima prioridad para el cargo de Analista IV en Asistencia al Usuario. Regula la identificación, ubicación y clasificación de sujetos pasivos de obligaciones administradas por la DIAN."
        )
        db.add(m1)
        db.flush()

        t1_1 = Topic(
            module_id=m1.id,
            title="Obligados, Formalización y Documentación Requerida",
            order=1,
            legal_basis="E.T. Art. 555-2, DUR 1625 de 2016 Art. 1.6.1.2.1 al 1.6.1.2.10",
            content="""### 1. Sujetos Obligados a Inscribirse en el RUT
Están obligados a inscribirse en el Registro Único Tributario (RUT):
- Las personas naturales y jurídicas que tengan la calidad de contribuyentes declarantes del impuesto sobre la renta y complementarios.
- Los sujetos pasivos del impuesto sobre las ventas (IVA) y del impuesto nacional al consumo.
- Los agentes retenedores en la fuente.
- Los importadores, exportadores y demás usuarios aduaneros.
- Los profesionales del cambio de divisas y comerciantes autorizados.
- Quienes deban expedir factura electrónica o documento equivalente.
- Personas no residentes con operaciones sujetas a tributación en Colombia.

### 2. Formalización de la Inscripción
La formalización es el proceso mediante el cual el administrado presenta ante la DIAN (virtual o presencialmente) los documentos soporte para obtener su número de identificación tributaria (NIT) y certificado definitivo.
- **Personas Naturales:** Cédula de ciudadanía original o digital; para menores de edad, tarjeta de identidad y representación de padres/tutores.
- **Personas Jurídicas:** Documento de constitución legal, certificado de existencia y representación legal (si aplica) expedido por la Cámara de Comercio con fecha de vigencia no superior a 30 días, documento de identidad del representante legal.
- **Sucesiones Ilíquidas:** Registro civil de defunción del causante, documento de identidad del causante y del apoderado o albacea con personería o auto judicial/escritura pública de apertura de la sucesión."""
        )
        t1_2 = Topic(
            module_id=m1.id,
            title="Actualización de Oficio vs. a Solicitud de Parte",
            order=2,
            legal_basis="DUR 1625 de 2016 Art. 1.6.1.2.14 y Art. 1.6.1.2.15",
            content="""### 1. Actualización a Solicitud de Parte
El obligado debe actualizar el RUT cuando ocurra cualquier modificación en los datos de:
- Ubicación (dirección, municipio, correo electrónico, teléfono).
- Clasificación (actividades económicas CIIU, responsabilidades tributarias).
- Representación legal o calidades aduaneras.

**Término Legal Obligatorio:** El obligado tiene un plazo máximo de **un (1) mes** siguiente al hecho que genera la actualización para formalizarla ante la DIAN (Art. 658-3 E.T.). El incumplimiento genera sanción pecuniaria por día de retraso.

### 2. Actualización de Oficio por la DIAN
La DIAN puede actualizar de oficio el RUT cuando:
- Obtenga información fiable por cruce de datos de terceros (Cámaras de Comercio, Notarías, Entidades Financieras, Registraduría).
- Detecte inconsistencias evidentes en visitas de fiscalización o cruces automáticos.
- Se determine cambio de domicilio fiscal no informado.
La actualización de oficio se notifica al administrado mediante los mecanismos previstos en el Estatuto Tributario."""
        )
        t1_3 = Topic(
            module_id=m1.id,
            title="Suspensión del RUT: Causales, Procedimiento y Levantamiento",
            order=3,
            legal_basis="DUR 1625 de 2016 Art. 1.6.1.2.16 y Art. 1.6.1.2.17",
            content="""### 1. Causales de Suspensión de la Inscripción en el RUT
La suspensión es una medida preventiva temporal que inhabilita el uso comercial o formal del RUT sin extinguir la persona. Procede por:
1. No ubicación del contribuyente en la dirección informada en visitas de verificación oficial.
2. Fallecimiento de la persona natural cuando no se ha iniciado el trámite de sucesión ilíquida.
3. Inconsistencias graves en los documentos de identificación o suplantación confirmada.
4. Información falsa o incompleta suministrada en el momento del registro.
5. Inactividad tributaria injustificada por más de cinco (5) años sin declaraciones presentadas.

### 2. Levantamiento de la Suspensión
Para levantar la suspensión:
- El administrado debe subsanar la causal que originó la medida (demostrar ubicación real mediante recibos públicos o contrato de arrendamiento, validar identidad biométrica presencial).
- Una vez radicada la solicitud y verificado el cumplimiento de requisitos, la DIAN dispone de un término legal de **diez (10) días hábiles** para emitir el acto que ordena el levantamiento en el sistema informático."""
        )
        t1_4 = Topic(
            module_id=m1.id,
            title="Cancelación Definitiva del RUT y Control de Obligaciones",
            order=4,
            legal_basis="DUR 1625 de 2016 Art. 1.6.1.2.18 al 1.6.1.2.20",
            content="""### 1. Causales de Cancelación Definitiva
La cancelación extingue definitivamente la inscripción en el registro:
- **Personas Naturales:** Liquidación final y adjudicación de la sucesión ilíquida mediante escritura pública o sentencia judicial debidamente ejecutoriada.
- **Personas Jurídicas:** Liquidación formal de la sociedad, fusión o absorción donde la entidad desaparece, o cancelación de la personería jurídica por autoridad competente.

### 2. Requisito Esencial: Verificación Previa de Obligaciones
La DIAN **no podrá conceder la cancelación del RUT** si el contribuyente presenta:
- Obligaciones tributarias, aduaneras o cambiarias pendientes de pago (cartera coactiva).
- Declaraciones omisas en períodos no prescritos.
- Procesos de fiscalización o liquidación oficial en curso sin fallo definitivo firme."""
        )
        db.add_all([t1_1, t1_2, t1_3, t1_4])

        # =========================================================================
        # MÓDULO 2: SISTEMA PQRSF, DERECHO DE PETICIÓN Y CPACA (Ley 1437/2011)
        # =========================================================================
        m2 = Module(
            number=2,
            title="PQRSF, Derecho de Petición y CPACA",
            subtitle="Ley 1755 de 2015 y Ley 1437 de 2011 (Código de Procedimiento Administrativo)",
            category="Funcional",
            priority="Alta",
            icon="clipboard-document-list",
            description="Términos legales perentorios, modalidades de petición, actos administrativos, notificaciones personales y electrónicas, recursos de reposición y apelación, y silencio administrativo."
        )
        db.add(m2)
        db.flush()

        t2_1 = Topic(
            module_id=m2.id,
            title="Términos Legales Exactos del Derecho de Petición (Ley 1755 de 2015)",
            order=1,
            legal_basis="Ley 1755 de 2015 (Sustitutiva del Título II CPACA Art. 14)",
            content="""### Términos Perentorios para Responder Peticiones
Toda petición deberá resolverse dentro de los siguientes plazos improrrogables:
1. **Petición de Interés General o Particular:** **15 días hábiles** siguientes a su recepción.
2. **Petición de Documentos o Información Pública:** **10 días hábiles**. 
   - *Regla de Oro (Silencio Positivo / Aceptación Tácita):* Si la entidad no da respuesta dentro del plazo de 10 días, se entenderá que la solicitud ha sido aceptada y no se podrá negar la entrega de dichos documentos al peticionario, debiendo entregarlos dentro de los **3 días siguientes** (salvo reserva legal expresa).
3. **Peticiones de Consulta Jurídica/Doctrinaria:** **30 días hábiles** siguientes a su recepción.
4. **Traslado por Incompetencia:** Si la DIAN no es competente, debe remitir la petición a la entidad competente dentro de los **5 días hábiles** siguientes e informar al peticionario.
5. **Requerimiento de Información Incompleta y Desistimiento Tácito:** Si la petición está incompleta, se le requerirá al ciudadano para que subsane en el plazo de **un (1) mes**. Si en dicho plazo no aporta lo requerido sin causa justificada, opera el **desistimiento tácito** y se archiva."""
        )
        t2_2 = Topic(
            module_id=m2.id,
            title="Diferencias Técnicas en el Sistema PQRSF",
            order=2,
            legal_basis="Ley 1437 de 2011 y directrices DAFP",
            content="""### Tipología de Requerimientos Ciudadanos
- **Petición:** Solicitud formal mediante la cual el ciudadano requiere reconocimiento de un derecho, prestación de un servicio, copias o información.
- **Queja:** Manifestación de protesta o inconformidad por la conducta irregular, descortesía o desatención de un servidor público en ejercicio de sus funciones.
- **Reclamo:** Inconformidad por la prestación indebida, defectuosa o tardía de un servicio oficial, o suspensión injustificada del mismo.
- **Sugerencia:** Propuesta de mejora formulada por el ciudadano para optimizar un proceso, trámite o servicio de la entidad.
- **Felicitación:** Manifestación de satisfacción ciudadana ante la calidad y calidez del servicio recibido.
- **Denuncia:** Puesta en conocimiento ante la autoridad de presuntas irregularidades, actos de corrupción o delitos cometidos por servidores públicos o ciudadanos (ej. contrabando o evasión fiscal)."""
        )
        t2_3 = Topic(
            module_id=m2.id,
            title="Régimen de Notificaciones y Recursos Administrativos (CPACA)",
            order=3,
            legal_basis="Ley 1437 de 2011 Arts. 66 al 82",
            content="""### 1. Formas de Notificación de los Actos Administrativos
- **Notificación Personal:** Se entrega copia íntegra y gratuita del acto administrativo al interesado o apoderado directamente en ventanilla o despacho.
- **Notificación Electrónica:** Procede cuando el administrado haya aceptado este medio expresamente o en cumplimiento del sistema informático oficial de la DIAN. Se entiende surtida a partir del envío del mensaje y el acceso certificado.
- **Notificación por Aviso:** Procede cuando no fuere posible la notificación personal al cabo de cinco (5) días del envío de la citación. Se publica en la página web institucional y en un lugar de acceso al público de la entidad por el término de **cinco (5) días**.

### 2. Recursos contra los Actos Administrativos
Salvo norma especial, contra los actos definitivos proceden:
- **Recurso de Reposición:** Ante el mismo funcionario que profirió la decisión para que la aclare, modifique o revoque.
- **Recurso de Apelación:** Ante el superior jerárquico o funcional con el mismo propósito.
- **Recurso de Queja:** Procede cuando se rechace el recurso de apelación, interponiéndose directamente ante el superior.
**Plazo de Interposición:** Se deben interponer por escrito dentro de los **diez (10) días hábiles** siguientes a la notificación del acto."""
        )
        db.add_all([t2_1, t2_2, t2_3])

        # =========================================================================
        # MÓDULO 3: ORIENTACIÓN NORMATIVA TACI Y CONCEPTOS FISCALES (Funcional Nivel 2)
        # =========================================================================
        m3 = Module(
            number=3,
            title="Orientación Normativa TACI y Conceptos Fiscales",
            subtitle="Marco Tributario, Aduanero, Cambiario e Internacional y Lucha contra el Fraude",
            category="Funcional",
            priority="Alta",
            icon="calculator",
            description="Obligación sustancial vs. formal, diferenciación técnica entre evasión, elusión y contrabando, principios de la tributación y estructura tributaria colombiana."
        )
        db.add(m3)
        db.flush()

        t3_1 = Topic(
            module_id=m3.id,
            title="Obligación Tributaria Sustancial vs. Formal",
            order=1,
            legal_basis="Estatuto Tributario Art. 1 al 10",
            content="""### 1. Obligación Sustancial
Tiene por objeto el **pago efectivo del tributo** (dar una suma de dinero al Estado). Nace al realizarse el hecho generador previsto taxativamente en la ley (ej. obtener renta gravable, realizar venta gravada con IVA).

### 2. Obligaciones Formales
Son los deberes instrumentales de hacer, no hacer o soportar impuestos por la ley para facilitar la fiscalización, control y recaudo por parte de la administración:
- Inscribirse y actualizar oportunamente el RUT.
- Presentar las declaraciones tributarias en los formularios oficiales y plazos legales.
- Expedir factura electrónica de venta con validación previa.
- Llevar contabilidad y conservar documentos de soporte por el término de firmeza.
- Suministrar información exógena magnética requerida por la DIAN.
- Atender requerimientos ordinarios y especiales de la autoridad tributaria."""
        )
        t3_2 = Topic(
            module_id=m3.id,
            title="Evasión, Elusión y Contrabando: Distinciones Técnicas",
            order=2,
            legal_basis="Estatuto Tributario Art. 869 y Código Penal Arts. 319, 434A y 434B",
            content="""### 1. Evasión Fiscal (Ilegalidad Manifiesta)
Conducta ilícita consciente y voluntaria orientada a no pagar o pagar menos tributos ocultando ingresos, simulando pasivos, falsificando facturas o deducciones inexistentes. Constituye infracción sancionatoria tributaria y, superados ciertos montos en UVT, delito penal contra el tesoro público.

### 2. Elusión Fiscal (Abuso en Materia Tributaria)
Uso artificioso o abusivo de formas jurídicas y vacíos normativos para evitar o reducir el impacto fiscal sin violar explícitamente la letra estricta de la ley, pero desnaturalizando su espíritu o sustancia económica. El Art. 869 del E.T. faculta a la DIAN para recaracterizar y reconfigurar la operación desconociendo el beneficio tributario indebido.

### 3. Contrabando (Aduanero)
- **Contrabando Abierto:** Ingreso o salida de mercancías del territorio aduanero nacional evadiendo completamente los controles de la autoridad aduanera (puertos no autorizados, trochas).
- **Contrabando Técnico:** Declaración formal de mercancías ante la aduana incurriendo en subfacturación deliberada, alteración de origen o clasificación arancelaria fraudulenta para pagar menos aranceles o IVA."""
        )
        t3_3 = Topic(
            module_id=m3.id,
            title="Impuestos Administrados y Régimen Simple (RST)",
            order=3,
            legal_basis="Estatuto Tributario Libro I a VI y Ley 2277 de 2022",
            content="""### Estructura Básica de Impuestos DIAN
- **Impuesto sobre la Renta:** Grava la totalidad de ingresos susceptibles de producir incremento neto del patrimonio en el año gravable.
- **Impuesto sobre las Ventas (IVA):** Impuesto indirecto de carácter real sobre el consumo en la venta de bienes, prestación de servicios o importación.
- **Retención en la Fuente:** Mecanismo acelerado de recaudo anticipado del impuesto en el momento en que se efectúa el pago o abono en cuenta.
- **Régimen Simple de Tributación (RST):** Modelo opcional de tributación que unifica el impuesto sobre la renta, el impuesto nacional al consumo y el ICA municipal en una sola declaración anual, buscando formalizar pequeñas unidades productivas reduciendo cargas formales."""
        )
        db.add_all([t3_1, t3_2, t3_3])

        # =========================================================================
        # MÓDULO 4: CANALES DE SERVICIO Y ATENCIÓN AL CIUDADANO (Funcional Nivel 2)
        # =========================================================================
        m4 = Module(
            number=4,
            title="Canales de Servicio y Atención al Ciudadano",
            subtitle="Protocolos Institucionales DIAN, Atención Preferencial y Transformación Digital",
            category="Funcional",
            priority="Alta",
            icon="chat-bubble-left-right",
            description="Políticas de atención multicanal (presencial, videoatención, agendamiento, kioscos, chatbot), Instrumento de Firma Electrónica (IFE), protocolos de accesibilidad e inclusión."
        )
        db.add(m4)
        db.flush()

        t4_1 = Topic(
            module_id=m4.id,
            title="Ecosistema de Canales de Atención DIAN",
            order=1,
            legal_basis="Manual de Servicio al Ciudadano DIAN y Ficha CC-AU-2010",
            content="""### Canales Habilitados en la DIAN
1. **Canal Presencial:** Puntos de contacto en Direcciones Seccionales a nivel nacional para atención personalizada bajo esquema de cita previa o ventanilla de turno.
2. **Videoatención:** Canal virtual interactivo donde un funcionario asiste al contribuyente en tiempo real mediante videollamada para trámites de RUT, orientación y desbloqueo de cuentas.
3. **Kioscos de Autogestión:** Terminales informáticas ubicadas en las sedes para que los usuarios sin computador realicen trámites guiados.
4. **Chatbot Institucional y Asistente Virtual:** Canal de respuesta automatizada 24/7 para consultas frecuentes e información de requisitos.
5. **Instrumento de Firma Electrónica (IFE):** Mecanismo de autenticación digital que reemplaza la firma litográfica en la presentación de declaraciones y documentos oficiales ante la DIAN."""
        )
        t4_2 = Topic(
            module_id=m4.id,
            title="Protocolo de Atención Diferencial y Prioritaria",
            order=2,
            legal_basis="Ley 1437 de 2011 Art. 5 Numeral 6 y Ley 1755 de 2015",
            content="""### Sujetos de Atención Prioritaria Obligatoria
Tendrán derecho a atención prioritaria y preferencial en todas las ventanillas y canales presenciales de la DIAN:
- Personas en situación de discapacidad física, visual, auditiva o cognitiva.
- Adultos mayores (personas de 60 años o más).
- Mujeres en estado de embarazo o con niños de brazos.
- Poblaciones en situación de extrema vulnerabilidad o víctimas de violencia con acreditación.

**Regla de Lenguaje Claro:** El servidor público en Asistencia al Usuario debe comunicarse en un lenguaje sencillo, claro, respetuoso y libre de tecnicismos excesivos, asegurando que el ciudadano comprenda plenamente sus derechos, requisitos y plazos."""
        )
        db.add_all([t4_1, t4_2])

        # =========================================================================
        # MÓDULO 5: TRANSPARENCIA, GESTIÓN DOCUMENTAL, MIPG Y CONSTITUCIÓN
        # =========================================================================
        m5 = Module(
            number=5,
            title="Transparencia, Gestión Documental, MIPG y Constitución",
            subtitle="Leyes 1712/2014, 594/2000, Modelo Integrado de Planeación y Gestión y Carta Política",
            category="Funcional",
            priority="Media",
            icon="document-magnifying-glass",
            description="Reserva legal tributaria (Art. 583 ET), información pública clasificada vs. reservada, ciclo vital documental, dimensiones del MIPG y principios constitucionales de la función administrativa."
        )
        db.add(m5)
        db.flush()

        t5_1 = Topic(
            module_id=m5.id,
            title="Transparencia y Reserva Tributaria (Ley 1712/2014 y Art. 583 E.T.)",
            order=1,
            legal_basis="Ley 1712 de 2014 y Estatuto Tributario Art. 583",
            content="""### 1. Principio de Máxima Publicidad y sus Excepciones
Toda información en poder del Estado es pública por defecto, salvo dos excepciones taxativas:
- **Información Pública Clasificada:** Aquella que pertenece al ámbito propio, particular y privado de una persona natural o jurídica (datos personales, intimidad, secretos comerciales, historias clínicas).
- **Información Pública Reservada:** Aquella legalmente protegida para salvaguardar intereses públicos primordiales (seguridad nacional, defensa, relaciones internacionales, investigaciones penales).

### 2. Reserva Tributaria Estricta (Art. 583 E.T.)
La información tributaria respecto de las bases gravables y la determinación privada de los impuestos en las declaraciones tiene **carácter de reserva estricta**.
Los funcionarios de la DIAN solo podrán suministrarla a los jueces de la República, autoridades penales con orden judicial o entidades públicas autorizadas expresamente por ley. La vulneración de la reserva tributaria acarrea destitución inmediata y responsabilidad penal."""
        )
        t5_2 = Topic(
            module_id=m5.id,
            title="Gestión Documental y Ciclo Vital del Documento (Ley 594 de 2000)",
            order=2,
            legal_basis="Ley 594 de 2000 (Ley General de Archivos)",
            content="""### Ciclo Vital de los Documentos
1. **Archivo de Gestión:** Documentación en trámite o sometida a continua utilización y consulta administrativa por la dependencia generadora.
2. **Archivo Central:** Documentación transferida desde los archivos de gestión cuya consulta es menos frecuente, pero que mantiene valor administrativo, fiscal o legal.
3. **Archivo Histórico:** Documentos transferidos desde el archivo central que, por su valor científico, cultural o histórico permanente, deben conservarse indefinidamente.

**Tablas de Retención Documental (TRD):** Listado de series y subseries con sus correspondientes tipos documentales, a los cuales se les asigna el tiempo de permanencia en cada etapa del ciclo vital."""
        )
        t5_3 = Topic(
            module_id=m5.id,
            title="MIPG y Constitución Política (Art. 209)",
            order=3,
            legal_basis="Decreto 1499 de 2017 y Constitución Política Arts. 23, 29, 209",
            content="""### 1. Modelo Integrado de Planeación y Gestión (MIPG)
El MIPG opera a través de **7 Dimensiones** y **19 Políticas de Gestión y Desempeño**:
1. Talento Humano (Corazón del modelo)
2. Direccionamiento Estratégico y Planeación
3. Gestión con Valores para el Resultado
4. Evaluación de Resultados
5. Información y Comunicación
6. Gestión del Conocimiento y la Innovación
7. Control Interno (Líneas de defensa MECI)

### 2. Principios Constitucionales de la Función Pública (Art. 209 C.P.)
La función administrativa está al servicio de los intereses generales y se desarrolla con fundamento en los principios de:
- **Igualdad, Moralidad, Eficacia, Economía, Celeridad, Imparcialidad y Publicidad** mediante la descentralización, delegación y desconcentración de funciones."""
        )
        db.add_all([t5_1, t5_2, t5_3])

        # =========================================================================
        # MÓDULO 6: COMPETENCIAS COMPORTAMENTALES E INTEGRIDAD (15% + 10%)
        # =========================================================================
        m6 = Module(
            number=6,
            title="Competencias Comportamentales e Integridad",
            subtitle="Ficha CC-AU-2010 y Código de Integridad de la DIAN",
            category="Comportamental",
            priority="Alta",
            icon="shield-check",
            description="Competencias laborales para nivel técnico (Orientación al usuario Nivel 3, Orientación al logro Nivel 3, Comportamiento ético Nivel 2, Comunicación efectiva Nivel 2, Trabajo en equipo y Adaptabilidad) y los 5 valores del Código de Integridad."
        )
        db.add(m6)
        db.flush()

        t6_1 = Topic(
            module_id=m6.id,
            title="Competencias Laborales Oficiales (Ficha CC-AU-2010)",
            order=1,
            legal_basis="Resolución 0067 de 2024 DIAN y Decreto 815 de 2018",
            content="""### Competencias Comportamentales del Cargo Analista IV
1. **Orientación al Usuario y al Ciudadano (Nivel 3):** Capacidad para dirigir las decisiones y acciones a la satisfacción de las necesidades de los usuarios, identificando sus requerimientos y superando sus expectativas dentro del marco ético y normativo.
2. **Orientación al Logro (Nivel 3):** Encaminar todas las acciones hacia la consecución de las metas con altos estándares de calidad, oportunidad y eficiencia.
3. **Comportamiento Ético (Nivel 2):** Actuar con rectitud, probidad, honestidad y transparencia, rechazando privilegios indebidos, dádivas o conflictos de interés.
4. **Comunicación Efectiva (Nivel 2):** Transmitir ideas, directrices e información con claridad, precisión y asertividad, tanto de forma verbal como escrita.
5. **Trabajo en Equipo y Colaboración:** Trabajar coordinadamente con los miembros del equipo para el logro de propósitos comunes."""
        )
        t6_2 = Topic(
            module_id=m6.id,
            title="Código de Integridad y Buen Gobierno DIAN",
            order=2,
            legal_basis="Resolución DIAN y Guía General DAFP",
            content="""### Los 5 Valores Fundamentales del Servidor DIAN
1. **Honestidad:** Actúo siempre con fundamento en la verdad, cumpliendo mis deberes con transparencia y rectitud, y favoreciendo siempre el interés general frente al particular.
2. **Respeto:** Reconozco, valoro y trato de manera digna a todas las personas, con sus virtudes y defectos, sin importar su labor, su procedencia, títulos o cualquier otra condición.
3. **Compromiso:** Soy consciente de la importancia de mi rol como servidor público y estoy en disposición permanente para comprender y resolver las necesidades de las personas con las que me relaciono en mis labores cotidianas.
4. **Diligencia:** Cumplo con los deberes, funciones y responsabilidades asignadas a mi cargo de la mejor manera posible, con atención, prontitud, destreza y eficiencia.
5. **Justicia:** Actúo con imparcialidad garantizando los derechos de las personas, con equidad, igualdad y sin discriminación alguna."""
        )
        db.add_all([t6_1, t6_2])

        # =========================================================================
        # BANCO DE PREGUNTAS EN JUICIO SITUACIONAL (3 OPCIONES A, B, C ESTRICTAS)
        # =========================================================================
        questions_data = [
            # --- MÓDULO 1: RUT (Funcional) ---
            {
                "module": m1,
                "category": "Funcional",
                "case_study": "Un contribuyente persona natural acude al punto de atención de la Seccional Medellín solicitando inscribirse en el RUT porque iniciará actividades de comercio minorista. Al presentar su documento, entrega una contraseña de cédula por duplicado con foto y código QR expedida hace dos semanas por la Registraduría Nacional, manifestando que aún no le entregan el plástico original.",
                "question_text": "De acuerdo con el Decreto 1625 de 2016 sobre formalización del RUT, ¿cuál es el procedimiento normativo exacto que debe aplicar el Analista IV?",
                "legal_reference": "DUR 1625 de 2016 Art. 1.6.1.2.11 y Circulares DIAN",
                "explanation": "La opción B es la correcta porque la normatividad tributaria y las directrices de la Registraduría avalan la contraseña oficial con código de verificación como documento de identificación válido provisional para la formalización del RUT de personas naturales. La opción A es incorrecta porque rechazar el trámite vulnera el derecho al acceso administrativo al tener soporte legal válido. La opción C es un distractor porque la DIAN no expide NITs provisionales sin formalizar la inscripción completa.",
                "options": [
                    ("A", "Rechazar el trámite de plano indicándole que es obligatorio presentar el plástico original de la cédula de ciudadanía.", False),
                    ("B", "Proceder con la formalización del RUT validando la contraseña expedida por la Registraduría y verificando la correspondencia biométrica o de datos en el sistema.", True),
                    ("C", "Asignarle un NIT provisional transitorio válido por 30 días mientras presenta la cédula física.", False)
                ]
            },
            {
                "module": m1,
                "category": "Funcional",
                "case_study": "Una sociedad comercial con domicilio en Tuluá cambió de representante legal y de domicilio fiscal el 15 de marzo. El nuevo representante legal radica los documentos de modificación en la DIAN el 28 de mayo del mismo año sin justificación de fuerza mayor o caso fortuito.",
                "question_text": "Conforme al Estatuto Tributario y al DUR 1625 de 2016, ¿qué consecuencia legal y procedimiento corresponde a esta situación?",
                "legal_reference": "Estatuto Tributario Art. 658-3 Numeral 3 y DUR 1625 Art. 1.6.1.2.14",
                "explanation": "La opción C es la correcta. El artículo 658-3 num. 3 del E.T. y el DUR 1625 de 2016 establecen que la actualización a solicitud de parte debe realizarse dentro del mes siguiente al hecho que la genera (15 de abril a más tardar). Al radicarse el 28 de mayo, el contribuyente incurre en la sanción por actualización extemporánea tasada por cada día de retraso. La opción A es falsa porque el plazo es de 1 mes, no de 90 días. La opción B es un distractor erróneo porque no se cancela el RUT por simple extemporaneidad.",
                "options": [
                    ("A", "Aceptar la actualización sin consecuencias económicas porque la ley confiere un plazo ordinario de noventa (90) días calendario.", False),
                    ("B", "Proceder a suspender y cancelar de oficio el RUT de la sociedad por incurrir en desacato de las obligaciones formales.", False),
                    ("C", "Realizar la actualización del registro advirtiendo que el obligado ha incurrido en la sanción por extemporaneidad prevista en el artículo 658-3 del Estatuto Tributario.", True)
                ]
            },
            {
                "module": m1,
                "category": "Funcional",
                "case_study": "En un operativo de control de la Dirección Seccional, los funcionarios visitaron en tres oportunidades el domicilio fiscal informado por un comerciante en su RUT. En todas las ocasiones los vecinos certificaron por escrito que el contribuyente nunca ha operado en ese inmueble y el predio se encuentra en obra negra abandonada.",
                "question_text": "¿Qué medida administrativa procede respecto al RUT del contribuyente y qué causal sustenta la decisión?",
                "legal_reference": "DUR 1625 de 2016 Art. 1.6.1.2.16 Numeral 1",
                "explanation": "La opción A es la correcta: procede la suspensión del RUT por la causal de no ubicación del contribuyente en el domicilio informado. La suspensión no extingue la persona jurídica o las obligaciones, sino que inhabilita temporalmente el registro hasta que demuestre su ubicación real. La opción B es errónea porque la cancelación definitiva solo procede por disolución/liquidación o sentencia de sucesión. La opción C es falsa porque la ley faculta a la DIAN para suspender de forma preventiva.",
                "options": [
                    ("A", "Expedir acto administrativo ordenando la suspensión de la inscripción en el RUT por la causal de no ubicación en la dirección informada.", True),
                    ("B", "Decretar la cancelación definitiva del NIT de oficio por extinción de las actividades comerciales.", False),
                    ("C", "Mantener activo el registro y limitarse a imponer una sanción económica sin alterar el estado del RUT.", False)
                ]
            },

            # --- MÓDULO 2: PQRSF Y CPACA (Funcional) ---
            {
                "module": m2,
                "category": "Funcional",
                "case_study": "El 2 de mayo un ciudadano radica una petición solicitando copias de los actos administrativos de carácter general proferidos por la DIAN durante el último trimestre. El 17 de mayo (habiendo transcurrido 11 días hábiles), la administración no ha expedido respuesta alguna ni ha comunicado motivos de prórroga.",
                "question_text": "De acuerdo con el artículo 14 de la Ley 1755 de 2015, ¿cuál es el efecto jurídico del silencio administrativo en este caso concreto?",
                "legal_reference": "Ley 1755 de 2015 Art. 14 Parágrafo y Numeral 1",
                "explanation": "La opción B es la respuesta correcta conforme a la Ley 1755 de 2015: para peticiones de documentos o información pública el término perentorio es de 10 días hábiles. Si no se resuelve en dicho lapso, opera la figura de la aceptación tácita (silencio positivo) y la administración no podrá negar la entrega de las copias, debiendo ponerlas a disposición del peticionario dentro de los 3 días siguientes. La opción A confunde el término general de 15 días con el especial de copias (10 días). La opción C es incorrecta porque el silencio negativo rige para solicitudes particulares de fondo bajo el CPACA ordinario.",
                "options": [
                    ("A", "La petición se encuentra aún en término legal porque toda solicitud ciudadana dispone de quince (15) días hábiles para ser resuelta.", False),
                    ("B", "Se entiende que la solicitud ha sido aceptada tácitamente, no pudiendo negarse la entrega de los documentos, debiendo entregarlos dentro de los 3 días siguientes.", True),
                    ("C", "Opera el silencio administrativo negativo y el ciudadano queda facultado para interponer de inmediato recurso de reposición.", False)
                ]
            },
            {
                "module": m2,
                "category": "Funcional",
                "case_study": "Un ciudadano fue notificado personalmente el lunes 3 de octubre de un acto administrativo particular y definitivo, expedido por un jefe de división de la Seccional dentro de una actuación administrativa general regida por el CPACA (no se trata de una liquidación oficial ni de una sanción tributaria, que tienen recurso propio en el Estatuto Tributario). El ciudadano desea impugnarlo ante el mismo funcionario que lo expidió.",
                "question_text": "Conforme a las disposiciones del CPACA (Ley 1437 de 2011), ¿cuál recurso debe interponer y dentro de qué plazo legal?",
                "legal_reference": "Ley 1437 de 2011 Art. 76",
                "explanation": "La opción A es la correcta: ante el mismo funcionario que profirió la decisión procede el recurso de reposición, y el plazo perentorio para interponerlo por escrito es de diez (10) días hábiles contados a partir del día siguiente a la notificación personal. La opción B es incorrecta porque la apelación se surte ante el superior y el plazo legal no es de 5 días. La opción C es incorrecta porque el plazo en sede administrativa general no es de un mes.",
                "options": [
                    ("A", "Recurso de reposición ante el mismo funcionario que expidió el acto, dentro de los diez (10) días hábiles siguientes a la notificación.", True),
                    ("B", "Recurso de apelación ante el superior funcional dentro de los cinco (5) días hábiles siguientes.", False),
                    ("C", "Recurso de queja ante el Director Seccional dentro del mes siguiente a la notificación.", False)
                ]
            },
            {
                "module": m2,
                "category": "Funcional",
                "case_study": "Un ciudadano radica una solicitud ciudadana en la ventanilla única de la Seccional de Arauca exigiendo que la DIAN clausure un establecimiento de comercio porque supuestamente arroja basuras al andén público y genera ruidos molestos a altas horas de la noche.",
                "question_text": "Al evidenciarse que la DIAN carece de competencia funcional sobre espacio público y convivencia ciudadana, ¿cuál es el procedimiento obligatorio según la Ley 1755 de 2015?",
                "legal_reference": "Ley 1755 de 2015 Art. 21",
                "explanation": "La opción C es la correcta: el artículo 21 de la Ley 1755 de 2015 establece taxativamente que si la autoridad a quien se dirige la petición no es competente, debe remitirla a la autoridad competente (en este caso la Alcaldía Municipal / Inspección de Policía) dentro de los cinco (5) días hábiles siguientes a su recepción y enviar copia de la comunicación remisoria al peticionario. Las opciones A y B violan el procedimiento reglado de traslado por incompetencia.",
                "options": [
                    ("A", "Archivar inmediatamente la petición por manifiesta impertinencia sin necesidad de emitir ningún pronunciamiento.", False),
                    ("B", "Responder al ciudadano dentro de los 15 días comunicándole que debe radicar una nueva petición por su propia cuenta ante la Alcaldía.", False),
                    ("C", "Remitir la petición a la autoridad competente (Inspección de Policía / Alcaldía) dentro de los 5 días siguientes e informar al peticionario.", True)
                ]
            },

            # --- MÓDULO 3: TACI Y CONCEPTOS FISCALES (Funcional) ---
            {
                "module": m3,
                "category": "Funcional",
                "case_study": "En una orientación tributaria, un contribuyente pregunta al Analista IV sobre la diferencia entre no facturar electrónicamente ingresos reales para no pagar IVA ni Renta, frente a constituir una figura asociativa amparada en vacíos normativos para diferir el impuesto a largo plazo.",
                "question_text": "¿Cómo debe tipificar técnicamente el servidor público ambas conductas a la luz de la doctrina tributaria colombiana?",
                "legal_reference": "Estatuto Tributario Art. 869 y Ley 2277 de 2022",
                "explanation": "La opción B es la respuesta técnicamente correcta. La omisión deliberada de ingresos y facturación constituye evasión tributaria (conducta ilegal sancionable penal y administrativamente). El uso artificioso de figuras jurídicas sin sustancia económica para aprovechar vacíos normativos constituye elusión fiscal, susceptible de cláusula antielusión (Art. 869 E.T.). La opción A confunde los conceptos invirtiendo su naturaleza. La opción C es errónea porque el contrabando se refiere al régimen aduanero de mercancías.",
                "options": [
                    ("A", "La primera conducta es elusión porque no hay violencia y la segunda es evasión por existir sofisticación legal.", False),
                    ("B", "La primera conducta es evasión fiscal (ilícita y punible) y la segunda corresponde a elusión fiscal (abuso de formas jurídicas sujeto a cláusula antielusión).", True),
                    ("C", "Ambas conductas se catalogan técnicamente como contrabando técnico de naturaleza cambiaria.", False)
                ]
            },
            {
                "module": m3,
                "category": "Funcional",
                "case_study": "Un comerciante que recién cumplió los requisitos para pertenecer al Régimen Simple de Tributación (RST) consulta si acogerse a este modelo lo exonera de presentar la declaración de retención en la fuente a título de renta cuando actúa como agente retenedor.",
                "question_text": "Atendiendo a la naturaleza de las obligaciones formales y sustanciales del Régimen Simple de Tributación, ¿cuál es la orientación correcta?",
                "legal_reference": "Estatuto Tributario Art. 911 y DUR 1625 Art. 1.5.8.3.1",
                "explanation": "La opción A es la correcta: los contribuyentes del Régimen Simple de Tributación no son sujetos pasivos de retención en la fuente a título de renta ni están obligados a practicar retenciones a título de renta a terceros (salvo retenciones por pagos laborales), pero deben cumplir plenamente las obligaciones formales propias del impuesto unificado y la facturación electrónica. La opción B es un error común que desconoce el beneficio legal de simplificación. La opción C distorsiona el régimen.",
                "options": [
                    ("A", "Como contribuyente del RST no está obligado a practicar retenciones a título de renta, salvo las derivadas de relaciones laborales, manteniendo sus deberes de facturación electrónica.", True),
                    ("B", "El RST elimina todas las obligaciones formales y sustanciales, incluyendo la expedición de factura electrónica.", False),
                    ("C", "Debe continuar presentando mensualmente todas las declaraciones ordinarias de retención sin ningún tipo de excepción.", False)
                ]
            },

            # --- MÓDULO 4: CANALES DE ATENCIÓN (Funcional) ---
            {
                "module": m4,
                "category": "Funcional",
                "case_study": "En la sala de espera presencial de la Seccional Tuluá se encuentra un ciudadano adulto mayor de 72 años con dificultad motriz evidente que no tiene cita previa en el sistema web. Simultáneamente, hay otros usuarios esperando turno con cita previamente agendada.",
                "question_text": "De acuerdo con el protocolo institucional de atención y la Ley 1437 de 2011, ¿qué acción debe ejecutar el Analista IV?",
                "legal_reference": "Ley 1437 de 2011 Art. 5 Numeral 6 y Protocolo de Servicio al Ciudadano DIAN",
                "explanation": "La opción C es la correcta: la ley y los protocolos estatales de atención al ciudadano obligan a brindar atención preferencial y prioritaria a adultos mayores y personas con discapacidad física, garantizando su atención aun sin cita previa a través del módulo de contingencia o priorización presencial, sin menoscabar el orden general de las demás citas. La opción A desconoce el mandato legal superior de atención preferencial. La opción B impone una barrera digital indebida a un sujeto de especial protección.",
                "options": [
                    ("A", "Negar el ingreso al área de atención y exigirle que se retire hasta que un familiar le agende una cita virtual.", False),
                    ("B", "Obligarlo a utilizar exclusivamente un kiosco de autogestión sin ningún tipo de acompañamiento personalizado.", False),
                    ("C", "Asignarle un turno de atención prioritaria y diferencial para resolver su trámite de manera expedita, brindándole la asistencia requerida.", True)
                ]
            },
            {
                "module": m4,
                "category": "Funcional",
                "case_study": "Un contribuyente obligado a declarar renta de forma virtual manifiesta en ventanilla que olvidó la clave de su Instrumento de Firma Electrónica (IFE) y que su declaración vence el mismo día a las 11:59 p.m. Solicita que el Analista IV le reciba la declaración en formulario físico litográfico firmado a mano.",
                "question_text": "¿Cuál es el procedimiento normativo aplicable respecto al Instrumento de Firma Electrónica (IFE) y los obligados virtuales?",
                "legal_reference": "Resolución DIAN 000070 de 2016 y Estatuto Tributario Art. 579-2",
                "explanation": "La opción B es la correcta: los obligados a declarar virtualmente deben hacerlo indefectiblemente a través de los Servicios Informáticos Electrónicos (SIE) con IFE; si la presentan en papel, se tendrá por no presentada (Art. 588 E.T.). El servidor debe orientarlo de inmediato en el procedimiento en línea o presencial de generación y recuperación de clave del IFE para que cumpla válidamente el mismo día.",
                "options": [
                    ("A", "Recibir el formulario físico litográfico con sello de ventanilla para evitar que incurra en extemporaneidad.", False),
                    ("B", "Informarle que la presentación física carece de validez legal para obligados virtuales y guiarlo inmediatamente en el proceso de restablecimiento del IFE a través de los canales digitales.", True),
                    ("C", "Firmar la declaración en el sistema informático utilizando la firma del propio funcionario para solucionar la urgencia del usuario.", False)
                ]
            },

            # --- MÓDULO 5: TRANSPARENCIA Y MIPG (Funcional) ---
            {
                "module": m5,
                "category": "Funcional",
                "case_study": "Un periodista se presenta en la Dirección Seccional con un carné de prensa y exige por escrito que se le entregue copia íntegra de la última declaración de renta de un reconocido candidato a la alcaldía municipal, invocando el principio de máxima publicidad de la Ley 1712 de 2014.",
                "question_text": "¿Cuál es la respuesta jurídica que debe suministrar la DIAN amparada en la normatividad vigente?",
                "legal_reference": "Estatuto Tributario Art. 583 y Ley 1712 de 2014 Art. 18",
                "explanation": "La opción B es la correcta. El artículo 583 del Estatuto Tributario consagra la reserva tributaria estricta sobre las declaraciones de impuestos y sus bases gravables, prevaleciendo como excepción legal amparada por la Ley 1712 de 2014 (información reservada y datos personales protegidos). El estatus de periodista no levanta la reserva tributaria. La opción A es ilegal y acarrearía destitución y delito penal para el funcionario. La opción C es incorrecta porque la reserva ampara a cualquier ciudadano independientemente de su cargo o aspiración política.",
                "options": [
                    ("A", "Entregar inmediatamente las copias solicitadas debido a que el libre ejercicio de la prensa prima sobre cualquier reserva institucional.", False),
                    ("B", "Negar la entrega de la declaración invocando la reserva tributaria estricta del artículo 583 del Estatuto Tributario y la protección de datos clasificados.", True),
                    ("C", "Entregar la información únicamente si el candidato autoriza verbalmente por llamada telefónica.", False)
                ]
            },
            {
                "module": m5,
                "category": "Funcional",
                "case_study": "En la dependencia de Asistencia al Usuario se acumulan expedientes físicos de peticiones y quejas tramitadas hace tres años. Un funcionario propone quemar o reciclar los expedientes para liberar espacio físico en la oficina sin consultar la Tabla de Retención Documental (TRD).",
                "question_text": "A la luz de la Ley General de Archivos (Ley 594 de 2000), ¿cómo debe procederse con esta documentación?",
                "legal_reference": "Ley 594 de 2000 y Acuerdo AGN 004 de 2019",
                "explanation": "La opción A es la correcta: ningún servidor público puede eliminar o destruir documentos sin agotar los tiempos de retención previstos en las TRD oficiales y sin la autorización formal del Comité Institucional de Gestión y Desempeño. Cumplido el tiempo en archivo de gestión, procede su transferencia primaria al archivo central.",
                "options": [
                    ("A", "Rechazar la propuesta y aplicar la Tabla de Retención Documental (TRD) para realizar la transferencia primaria al archivo central conforme a los plazos legales.", True),
                    ("B", "Proceder a la destrucción inmediata siempre y cuando se levante un acta interna firmada por dos testigos.", False),
                    ("C", "Entregar los expedientes a una empresa de reciclaje dejando constancia en un libro de minutas de la oficina.", False)
                ]
            },

            # --- MÓDULO 6: COMPORTAMENTALES E INTEGRIDAD (Comportamental e Integridad) ---
            {
                "module": m6,
                "category": "Comportamental",
                "case_study": "En una jornada de alta congestión por vencimientos tributarios, el sistema informático de la DIAN presenta intermitencia y lentitud generalizada. Los ciudadanos en la fila comienzan a mostrar impaciencia y reclamos airados hacia los funcionarios en ventanilla.",
                "question_text": "Frente a la competencia de 'Orientación al Usuario y al Ciudadano (Nivel 3)' de la ficha CC-AU-2010, ¿cuál es la conducta esperada del Analista IV?",
                "legal_reference": "Ficha de Funciones CC-AU-2010 y Guía de Competencias DAFP",
                "explanation": "La opción A demuestra un comportamiento en Nivel 3 de Orientación al Ciudadano: mantener la serenidad, informar proactivamente con asertividad y empatía sobre la contingencia técnica, y adelantar la revisión física de documentos para optimizar el tiempo mientras se restablece el servicio. La opción B es reactiva y defensiva. La opción C elude la responsabilidad delegando el conflicto en seguridad.",
                "options": [
                    ("A", "Informar de manera clara y empática la situación técnica, verificar previamente los documentos de los usuarios en fila para agilizar el trámite cuando el sistema responda, manteniendo una actitud conciliadora.", True),
                    ("B", "Suspender la atención en ventanilla y contestar a los usuarios que la entidad no tiene la culpa de los fallos tecnológicos del servidor central.", False),
                    ("C", "Llamar al personal de vigilancia privada para que desaloje la sala y exigir silencio absoluto antes de continuar.", False)
                ]
            },
            {
                "module": m6,
                "category": "Comportamental",
                "case_study": "El jefe de dependencia asigna al equipo la meta de reducir en un 30% los tiempos de espera en ventanilla durante el próximo mes. El Analista IV detecta que los ciudadanos pierden tiempo diligenciando borradores equivocados antes de llegar al módulo de atención.",
                "question_text": "Bajo la competencia de 'Orientación al Logro (Nivel 3)', ¿cuál es la iniciativa más adecuada para alcanzar la meta fijada?",
                "legal_reference": "Ficha CC-AU-2010 (Competencias Conductuales DAFP)",
                "explanation": "La opción C refleja la competencia de Orientación al Logro en Nivel 3: identificar cuellos de botella en la operación y proponer e implementar proactivamente soluciones sistemáticas (como guías visuales o filtros previos) para elevar el rendimiento colectivo y superar las metas trazadas. Las opciones A y B son pasivas y no generan mejoras en los procesos.",
                "options": [
                    ("A", "Limitarse a atender más rápido a cada usuario recortando la información suministrada sobre sus derechos tributarios.", False),
                    ("B", "Esperar a que finalice el mes para presentar un informe quejándose de los errores cometidos por los ciudadanos.", False),
                    ("C", "Proponer al equipo implementar un filtro orientador inicial y fichas gráficas en la sala de espera para que los usuarios preparen sus documentos antes de ser llamados.", True)
                ]
            },
            {
                "module": m6,
                "category": "Integridad",
                "case_study": "Un conocido tramitador de la ciudad se acerca a la ventanilla del Analista IV al finalizar la jornada laboral y le ofrece una bonificación económica en efectivo a cambio de que agilice la expedición del RUT de diez clientes suyos sin que estos deban solicitar cita previa ni hacer fila.",
                "question_text": "Bajo los mandatos del Código de Integridad de la DIAN y el principio de Comportamiento Ético, ¿cuál debe ser la actuación inmediata e ineludible del servidor público?",
                "legal_reference": "Código de Integridad DIAN (Valor Honestidad) y Ley 1952 de 2019",
                "explanation": "La opción C es la única correcta: el valor de la Honestidad y el deber legal exigen rechazar tajantemente cualquier ofrecimiento de dádivas o ventajas indebidas y poner la conducta en conocimiento de las autoridades competentes y de control interno disciplinario. La opción A incurre en el delito de cohecho. La opción B normaliza la corrupción al limitarse al silencio pasivo.",
                "options": [
                    ("A", "Aceptar la bonificación siempre y cuando se realice por fuera de las instalaciones de la entidad y los documentos cumplan con los requisitos formales.", False),
                    ("B", "Rechazar verbalmente el dinero pero prestar el servicio de agilización por cortesía y amistad con el tramitador.", False),
                    ("C", "Rechazar de manera rotunda el ofrecimiento económico e informar de inmediato el hecho ante la dependencia de Control Interno Disciplinario y las autoridades penales pertinentes.", True)
                ]
            }
        ]

        for q_data in questions_data:
            q = Question(
                module_id=q_data["module"].id,
                category=q_data["category"],
                case_study=q_data["case_study"],
                question_text=q_data["question_text"],
                explanation=q_data["explanation"],
                legal_reference=q_data["legal_reference"]
            )
            db.add(q)
            db.flush()

            for letter, opt_text, is_corr in q_data["options"]:
                opt = Option(
                    question_id=q.id,
                    letter=letter,
                    text=opt_text,
                    is_correct=is_corr
                )
                db.add(opt)

        # =========================================================================
        # FLASHCARDS DE ALTO RENDIMIENTO (MEMORIZACIÓN DE PLAZOS Y NORMAS)
        # =========================================================================
        flashcards_data = [
            (m1, "Término para actualizar el RUT a solicitud de parte", "Máximo un (1) mes siguiente al hecho que genera la modificación.", "Art. 658-3 Numeral 3 Estatuto Tributario", "Plazos Legales"),
            (m1, "Término para resolver levantamiento de suspensión del RUT", "Diez (10) días hábiles siguientes a la radicación de la subsanación.", "DUR 1625 de 2016 Art. 1.6.1.2.17", "Plazos Legales"),
            (m2, "Plazo para resolver Peticiones de Documentos o Información", "Diez (10) días hábiles. Si no se resuelve, opera la aceptación tácita y deben entregarse a los 3 días.", "Ley 1755 de 2015 Art. 14", "Plazos Legales"),
            (m2, "Plazo para resolver Peticiones de Consulta Doctrinal", "Treinta (30) días hábiles siguientes a su recepción.", "Ley 1755 de 2015 Art. 14", "Plazos Legales"),
            (m2, "Plazo de traslado por incompetencia a otra entidad", "Cinco (5) días hábiles siguientes a la recepción de la petición.", "Ley 1755 de 2015 Art. 21", "Plazos Legales"),
            (m2, "Plazo para interponer Recursos de Reposición y Apelación", "Diez (10) días hábiles contados a partir del día siguiente a la notificación del acto.", "Ley 1437 de 2011 Art. 76 (CPACA)", "Plazos Legales"),
            (m2, "Término del desistimiento tácito en peticiones incompletas", "Un (1) mes para que el ciudadano subsane lo requerido.", "Ley 1755 de 2015 Art. 17", "Plazos Legales"),
            (m3, "Obligación Tributaria Sustancial", "Vínculo jurídico que tiene por objeto el pago efectivo del tributo (dar una suma de dinero al Estado).", "Estatuto Tributario Art. 1", "Conceptos Fiscales"),
            (m3, "Evasión Fiscal vs. Elusión Fiscal", "Evasión es ilegal (ocultamiento/fraude). Elusión es abuso de formas jurídicas para reducir tributos sin infringir literalmente la ley.", "E.T. Art. 869", "Conceptos Fiscales"),
            (m4, "Instrumento de Firma Electrónica (IFE)", "Mecanismo digital que sustituye la firma autógrafa para cumplir obligaciones tributarias y aduaneras en los SIE.", "Resolución 000070 de 2016", "Canales DIAN"),
            (m4, "Sujetos de Atención Prioritaria Obligatoria", "Adultos mayores (≥ 60 años), personas en situación de discapacidad, mujeres gestantes y niños de brazos.", "Ley 1437 Art. 5 Num. 6", "Servicio al Usuario"),
            (m5, "Reserva Tributaria Estricta", "Las bases gravables y la determinación privada de los impuestos en las declaraciones tributarias son estrictamente reservadas.", "Estatuto Tributario Art. 583", "Normativa"),
            (m5, "Ciclo Vital del Documento", "Archivo de Gestión (trámite activo) -> Archivo Central (semi-activo / fiscal) -> Archivo Histórico (patrimonio permanente).", "Ley 594 de 2000", "Gestión Documental"),
            (m6, "Valores del Código de Integridad DIAN", "Honestidad, Respeto, Compromiso, Diligencia y Justicia.", "Código de Integridad y Buen Gobierno DIAN", "Integridad"),
            (m6, "Orientación al Usuario y al Ciudadano (Nivel 3)", "Capacidad para dirigir decisiones y acciones a resolver y superar las necesidades del ciudadano dentro de la ética y la norma.", "Ficha CC-AU-2010", "Competencias")
        ]

        for mod, term, definition, norm, cat in flashcards_data:
            fc = Flashcard(
                module_id=mod.id,
                term=term,
                definition=definition,
                legal_norm=norm,
                category=cat
            )
            db.add(fc)

        db.commit()

        # Contenido ampliado según los 14 ejes temáticos de la ficha CC-AU-2010
        seed_extended_content(db)
        SeedService.set_content_version(db, CONTENT_VERSION)
