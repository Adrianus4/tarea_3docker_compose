from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("evaluar/", views.upload_image, name="upload"),
    path("historial/", views.history, name="history"),
]
