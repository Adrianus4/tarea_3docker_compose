from django.test import SimpleTestCase

from .services import classify_risk, normalize_probability


class RiskClassificationTests(SimpleTestCase):
    def test_low_risk_below_40_percent(self):
        self.assertEqual(classify_risk(0.399)[0], "bajo")

    def test_moderate_risk_includes_40_and_70_percent(self):
        self.assertEqual(classify_risk(0.4)[0], "moderado")
        self.assertEqual(classify_risk(0.7)[0], "moderado")

    def test_high_risk_above_70_percent(self):
        self.assertEqual(classify_risk(0.701)[0], "alto")

    def test_probability_is_clamped(self):
        self.assertEqual(normalize_probability([[1.4]]), 1.0)
        self.assertEqual(normalize_probability([[-0.2]]), 0.0)
