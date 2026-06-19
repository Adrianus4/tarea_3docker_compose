from django.conf import settings
from django.db import models


class ScreeningResult(models.Model):
    RISK_LOW = "bajo"
    RISK_MODERATE = "moderado"
    RISK_HIGH = "alto"

    RISK_CHOICES = [
        (RISK_LOW, "Bajo"),
        (RISK_MODERATE, "Moderado"),
        (RISK_HIGH, "Alto"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_filename = models.CharField(max_length=255)
    probability = models.FloatField()
    risk_level = models.CharField(max_length=20, choices=RISK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.risk_level} - {self.probability:.3f}"

    @property
    def probability_percent(self):
        return self.probability * 100
