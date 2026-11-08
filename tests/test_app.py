"""
Pruebas de regresión y de calidad de contenido (Raphael · QA).
Ejecutar desde prepdian_app/:   python -m unittest discover -s tests -v
Usa una BD temporal: NUNCA toca prepdian.db.
"""
import os
import re
import sqlite3
import tempfile
import unittest

_TMP_DIR = tempfile.mkdtemp(prefix="prepdian_test_")
os.environ["PREPDIAN_DB_PATH"] = os.path.join(_TMP_DIR, "test.db")

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402
from app.core.database import SessionLocal  # noqa: E402
from app.models.models import Module, Question, ExamAttempt  # noqa: E402
from app.services.content_opec import EJES_OPEC, CONTENT_VERSION  # noqa: E402
from app.services.seed_service import SeedService  # noqa: E402


class PrepDIANTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ctx = TestClient(app)
        cls.client = cls.ctx.__enter__()  # dispara lifespan → crea tablas y siembra

    @classmethod
    def tearDownClass(cls):
        cls.ctx.__exit__(None, None, None)

    # ---------------- Contrato de la API original (cero regresiones) ----------------
    def test_endpoints_originales_responden(self):
        for url in ["/", "/api/convocatoria", "/api/modules", "/api/flashcards",
                    "/api/documents", "/api/v1/documents", "/api/exam/statistics",
                    "/api/exam/questions", "/favicon.ico"]:
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200, url)

    def test_exam_sin_parametros_devuelve_todas_en_orden(self):
        qs = self.client.get("/api/exam/questions").json()
        ids = [q["id"] for q in qs]
        self.assertEqual(ids, sorted(ids))
        db = SessionLocal()
        try:
            self.assertEqual(len(ids), db.query(Question).count())
        finally:
            db.close()

    def test_exam_no_revela_respuesta_correcta(self):
        for q in self.client.get("/api/exam/questions?limit=30").json():
            for opt in q["options"]:
                self.assertIsNone(opt["is_correct"])

    # ---------------- Calidad del banco de preguntas ----------------
    def test_cada_pregunta_tiene_A_B_C_y_una_sola_correcta(self):
        db = SessionLocal()
        try:
            for q in db.query(Question).all():
                letters = sorted(o.letter for o in q.options)
                self.assertEqual(letters, ["A", "B", "C"], f"Pregunta {q.id}")
                self.assertEqual(sum(o.is_correct for o in q.options), 1, f"Pregunta {q.id}")
        finally:
            db.close()

    def test_explicacion_coincide_con_la_clave(self):
        """Ataque adversarial: si la explicación dice 'La opción X es la correcta',
        X debe ser la opción marcada como correcta."""
        pat = re.compile(r"[Oo]pci[oó]n ([ABC]) (?:es|demuestra|refleja)")
        db = SessionLocal()
        try:
            for q in db.query(Question).all():
                correct = next(o.letter for o in q.options if o.is_correct)
                m = pat.search(q.explanation)
                self.assertIsNotNone(m, f"Pregunta {q.id} sin letra en la explicación")
                self.assertEqual(m.group(1), correct, f"Pregunta {q.id}: explicación dice {m.group(1)}, clave {correct}")
        finally:
            db.close()

    def test_claves_distribuidas_sin_sesgo(self):
        db = SessionLocal()
        try:
            counts = {"A": 0, "B": 0, "C": 0}
            for q in db.query(Question).all():
                counts[next(o.letter for o in q.options if o.is_correct)] += 1
            total = sum(counts.values())
            for letter, n in counts.items():
                self.assertGreater(n / total, 0.2, f"Clave {letter} subrepresentada: {counts}")
        finally:
            db.close()

    def test_banco_ampliado(self):
        db = SessionLocal()
        try:
            self.assertGreaterEqual(db.query(Question).count(), 80)
            self.assertEqual(db.query(Module).count(), 12)
            for m in db.query(Module).all():
                self.assertGreater(len(m.topics), 0, m.title)
                self.assertGreater(len(m.questions), 0, m.title)
        finally:
            db.close()

    def test_error_reposicion_vs_reconsideracion_corregido(self):
        db = SessionLocal()
        try:
            for q in db.query(Question).all():
                correct = next(o for o in q.options if o.is_correct)
                if "liquidación oficial" in q.case_study and "Reposición" in correct.text:
                    self.fail(f"Pregunta {q.id}: reposición como recurso contra liquidación oficial")
        finally:
            db.close()

    # ---------------- Ejes OPEC ----------------
    def test_ejes_cubren_los_14_de_la_ficha_y_enlazan_modulos(self):
        data = self.client.get("/api/ejes").json()
        ejes = data["ejes"]
        self.assertEqual(len([e for e in ejes if e["numero"] <= 14]), 14)
        module_ids = {m["id"] for m in self.client.get("/api/modules").json()}
        for e in ejes:
            self.assertTrue(e["modulos"], e["titulo"])
            for m in e["modulos"]:
                self.assertIn(m["id"], module_ids)
            self.assertGreater(e["questions_count"], 0, e["titulo"])
        self.assertIn("2026-11-08", data["fecha_prueba"])

    # ---------------- Simulacro configurable ----------------
    def test_limit_balanceado_y_sin_duplicados(self):
        qs = self.client.get("/api/exam/questions?limit=24").json()
        self.assertEqual(len(qs), 24)
        self.assertEqual(len({q["id"] for q in qs}), 24)
        self.assertGreaterEqual(len({q["module_id"] for q in qs}), 10)

    def test_filtro_por_modulos(self):
        mods = self.client.get("/api/modules").json()
        target = [m["id"] for m in mods[:2]]
        qs = self.client.get(f"/api/exam/questions?module_ids={target[0]},{target[1]}&shuffle=true").json()
        self.assertTrue(qs)
        self.assertTrue(all(q["module_id"] in target for q in qs))

    def test_parametros_invalidos(self):
        self.assertEqual(self.client.get("/api/exam/questions?module_ids=abc").status_code, 422)
        self.assertEqual(self.client.get("/api/exam/questions?limit=0").status_code, 422)
        self.assertEqual(self.client.get("/api/exam/questions?limit=-5").status_code, 422)
        self.assertEqual(self.client.get("/api/exam/questions?module_ids=99999").json(), [])

    def test_submit_calificacion_perfecta_y_vacia(self):
        db = SessionLocal()
        try:
            qs = db.query(Question).all()
            perfect = [{"question_id": q.id, "selected_option_id": next(o.id for o in q.options if o.is_correct)} for q in qs]
            blank = [{"question_id": q.id, "selected_option_id": None} for q in qs]
        finally:
            db.close()
        r = self.client.post("/api/exam/submit", json={"duration_seconds": 60, "answers": perfect}).json()
        self.assertEqual(r["functional_score"], 100.0)
        self.assertTrue(r["passed_functional"])
        r = self.client.post("/api/exam/submit", json={"duration_seconds": 60, "answers": blank}).json()
        self.assertEqual(r["functional_score"], 0.0)
        self.assertFalse(r["passed_functional"])

    # ---------------- Migración de versión (no perder historial) ----------------
    def test_cambio_de_version_resiembra_y_conserva_historial(self):
        db = SessionLocal()
        try:
            before_attempts = db.query(ExamAttempt).count()
            SeedService.set_content_version(db, "version-vieja")
            SeedService.seed_database(db)
            self.assertEqual(SeedService.get_content_version(db), CONTENT_VERSION)
            self.assertEqual(db.query(ExamAttempt).count(), before_attempts)
            self.assertEqual(db.query(Module).count(), 12)
            # Idempotencia: sembrar de nuevo no duplica
            n = db.query(Question).count()
            SeedService.seed_database(db)
            self.assertEqual(db.query(Question).count(), n)
        finally:
            db.close()

    def test_biblioteca_sin_dominios_rotos(self):
        """Dominios verificados como rotos o inaccesibles (404 / timeout)."""
        rotos = ["secretariasenado.gov.co", "archivogeneral.gov.co/transparencia",
                 "estatuto.co", "norma.php?i=82582"]
        docs = self.client.get("/api/documents").json()
        self.assertGreaterEqual(len(docs), 16)
        for d in docs:
            self.assertTrue(d["external_url"].startswith("https://"), d["title"])
            for r in rotos:
                self.assertNotIn(r, d["external_url"], d["title"])

    def test_bd_real_no_fue_tocada_por_las_pruebas(self):
        self.assertTrue(os.environ["PREPDIAN_DB_PATH"].startswith(_TMP_DIR))


if __name__ == "__main__":
    unittest.main(verbosity=2)
