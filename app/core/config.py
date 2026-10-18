import os

class Settings:
    PROJECT_NAME: str = "PrepDIAN 2676 - Analista IV (OPEC 236799)"
    PROJECT_VERSION: str = "1.0.0"
    
    # Datos oficiales de la convocatoria
    PROCESO: str = "Selección DIAN 2676 - Ingreso"
    CARGO: str = "Analista IV"
    NIVEL: str = "Técnico"
    GRADO: int = 4
    CODIGO: int = 204
    OPEC: int = 236799
    MANUAL_FUNCIONES_FICHA: str = "CC-AU-2010 (Resolución 0067 de 2024)"
    PROCESO_SUBPROCESO: str = "Cercanía con el ciudadano / Asistencia al usuario"
    VACANTES: int = 3
    CIUDADES_VACANTES: list = ["Medellín", "Tuluá", "Arauca"]
    
    # Reglas de Ponderación Oficiales
    WEIGHT_FUNCTIONAL: float = 0.65       # 65% Eliminatoria
    WEIGHT_BEHAVIORAL: float = 0.15       # 15% Clasificatoria
    WEIGHT_INTEGRITY: float = 0.10        # 10% Clasificatoria
    WEIGHT_BACKGROUND: float = 0.10       # 10% Clasificatoria (Antecedentes)
    
    MIN_FUNCTIONAL_SCORE: float = 70.0    # Mínimo para no ser eliminado en la prueba funcional
    
    # SQLite DB Path
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DB_PATH: str = os.path.join(BASE_DIR, "prepdian.db")
    DATABASE_URL: str = f"sqlite:///{DB_PATH}"

settings = Settings()
