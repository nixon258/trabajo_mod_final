#!/usr/bin/env python3
"""Pruebas del modelo prospectivo. Ejecutar: python test_modelo_futuro.py"""
import json
import os
import unittest

import numpy as np

import modelo_futuro as m

DIR = os.path.dirname(os.path.abspath(__file__))


class TestModeloFuturo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.r = m.correr(replicas=40)

    def test_horizonte(self):
        self.assertEqual(len(self.r["Tendencial"]["trayectoria"]), m.MESES)

    def test_serie_valida(self):
        serie, miedo, mat = m.simular(dict(m.P), semilla=1)
        self.assertEqual(len(serie), m.MESES)
        self.assertTrue(np.all(serie >= 0))
        self.assertTrue(np.all((miedo >= 0) & (miedo <= 1)))
        self.assertTrue(np.all(mat >= 0))

    def test_orden_de_escenarios(self):
        base = self.r["Tendencial"]["total_5_anios"]
        fin60 = self.r["Financiamiento -60 %"]["total_5_anios"]
        fin80 = self.r["Financiamiento -80 %"]["total_5_anios"]
        self.assertLess(fin60, base)
        self.assertLess(fin80, fin60)

    def test_evitados_en_rango(self):
        for nombre, datos in self.r.items():
            self.assertGreaterEqual(datos["evitados_pct"], 0)
            self.assertLessEqual(datos["evitados_pct"], 100)

    def test_reproducibilidad(self):
        a = m.simular(dict(m.P), semilla=7)[0]
        b = m.simular(dict(m.P), semilla=7)[0]
        np.testing.assert_array_equal(a, b)

    def test_json_publicado(self):
        ruta = os.path.join(DIR, "resultados_futuro.json")
        if not os.path.exists(ruta):
            self.skipTest("JSON no generado")
        with open(ruta, encoding="utf-8") as fh:
            datos = json.load(fh)
        self.assertEqual(datos["meses"], 60)
        self.assertIn("Tendencial", datos["escenarios"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
