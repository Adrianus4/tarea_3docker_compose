from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from screening.forms import StyledAuthenticationForm
from screening import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "login/",
        LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=StyledAuthenticationForm,
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registro/", views.register, name="register"),
    path("healthz/", views.health_check, name="health_check"),
    path("", include("screening.urls")),
]
