import base64

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from .forms import ImageUploadForm, SignUpForm
from .models import ScreeningResult
from .services import ModelUnavailable, predict_anemia_risk


def home(request):
    if request.user.is_authenticated:
        return redirect("upload")
    return redirect("login")


def register(request):
    if request.user.is_authenticated:
        return redirect("upload")

    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Cuenta creada. Ya puedes realizar un tamizaje.")
        return redirect("upload")

    return render(request, "registration/register.html", {"form": form})


@login_required
def upload_image(request):
    form = ImageUploadForm()
    recent_results = ScreeningResult.objects.filter(user=request.user)[:5]

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            image_bytes = image.read()
            try:
                result = predict_anemia_risk(image_bytes)
            except ModelUnavailable as exc:
                messages.error(request, str(exc))
                return render(
                    request,
                    "screening/upload.html",
                    {"form": form, "recent_results": recent_results},
                    status=503,
                )
            except Exception:
                messages.error(request, "No se pudo procesar la imagen. Intenta con otra fotografia ocular.")
                return render(
                    request,
                    "screening/upload.html",
                    {"form": form, "recent_results": recent_results},
                    status=400,
                )

            record = ScreeningResult.objects.create(
                user=request.user,
                original_filename=image.name[:255],
                probability=result.probability,
                risk_level=result.risk_level,
            )
            preview_uri = build_preview_uri(image_bytes, image.content_type)
            return render(
                request,
                "screening/result.html",
                {
                    "result": result,
                    "record": record,
                    "preview_uri": preview_uri,
                },
            )

    return render(request, "screening/upload.html", {"form": form, "recent_results": recent_results})


@login_required
def history(request):
    results = ScreeningResult.objects.filter(user=request.user)[:25]
    return render(request, "screening/history.html", {"results": results})


@require_GET
def health_check(request):
    return JsonResponse({"status": "ok"})


def build_preview_uri(image_bytes: bytes, content_type: str) -> str:
    encoded = base64.b64encode(image_bytes).decode("ascii")
    return f"data:{content_type};base64,{encoded}"
