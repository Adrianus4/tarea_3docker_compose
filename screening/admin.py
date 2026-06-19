from django.contrib import admin

from .models import ScreeningResult


@admin.register(ScreeningResult)
class ScreeningResultAdmin(admin.ModelAdmin):
    list_display = ("user", "risk_level", "probability_percent", "original_filename", "created_at")
    list_filter = ("risk_level", "created_at")
    search_fields = ("user__username", "original_filename")
    readonly_fields = ("user", "probability", "risk_level", "original_filename", "created_at")

    @admin.display(description="Probabilidad")
    def probability_percent(self, obj):
        return f"{obj.probability * 100:.1f}%"
