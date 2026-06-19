from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class StyledAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "placeholder": "Ingresa tu usuario",
            }
        ),
    )
    password = forms.CharField(
        label="Contrasena",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Ingresa tu contrasena",
            }
        ),
    )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Correo", required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "Usuario",
            "password1": "Contrasena",
            "password2": "Confirmar contrasena",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Crea un usuario"})
        self.fields["email"].widget.attrs.update({"placeholder": "correo@ejemplo.com"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Minimo 8 caracteres"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Repite tu contrasena"})


class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="Imagen ocular")

    allowed_content_types = {"image/jpeg", "image/png", "image/webp"}

    def clean_image(self):
        image = self.cleaned_data["image"]
        content_type = getattr(image, "content_type", "")
        if content_type and content_type not in self.allowed_content_types:
            raise forms.ValidationError("Sube una imagen JPG, PNG o WEBP.")
        if image.size > settings.MAX_UPLOAD_BYTES:
            limit_mb = settings.MAX_UPLOAD_BYTES / (1024 * 1024)
            raise forms.ValidationError(f"La imagen no debe superar {limit_mb:.0f} MB.")
        return image
