<<<<<<< HEAD
# AnemiCheck MVP

MVP Django para tamizaje orientativo de anemia a partir de una imagen ocular.

## Flujo

- Login y registro basico.
- Subida de imagen JPG, PNG o WEBP.
- Backend convierte la imagen a RGB, la redimensiona a `224x224`, ejecuta `anemicheck_mobilenetv2_mvp.keras` y devuelve probabilidad + riesgo.
- Riesgo bajo: `<40%`, moderado: `40%-70%`, alto: `>70%`.
- El resultado siempre se presenta como tamizaje orientativo, no diagnostico medico.

## Local

Usa Python `3.11.9` para compatibilidad con `tensorflow-cpu`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

En Windows puedes usar `py`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
Copy-Item .env.example .env
py manage.py migrate
py manage.py runserver
```

## Generar DJANGO_SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

En Windows:

```powershell
py -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Render

Build command:

```bash
bash build.sh
```

Start command:

```bash
python manage.py migrate && gunicorn anemicheck.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

Variables de entorno:

- `DJANGO_SECRET_KEY`: valor generado con el comando anterior.
- `DEBUG`: `False`.
- `PYTHON_VERSION`: `3.11.9`.
- `DATABASE_URL`: Internal Database URL de Render Postgres.
- `ALLOWED_HOSTS`: dominio de Render, por ejemplo `tu-app.onrender.com`.
- `CSRF_TRUSTED_ORIGINS`: origen HTTPS, por ejemplo `https://tu-app.onrender.com`.
- `ANEMIA_MODEL_PATH`: `anemicheck_mobilenetv2_mvp.keras`.
- `MAX_UPLOAD_BYTES`: `6291456`.
- `SECURE_SSL_REDIRECT`: opcional, `False` por defecto porque Render ya termina HTTPS.
=======
# tarea_3docker_compose
>>>>>>> cae72236d7ba5bf3647e6ea18ba4e960cc31e614
