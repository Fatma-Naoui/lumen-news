@echo off
echo ========================================
echo Lumen News - Quick Project Setup
echo Creating entire project structure...
echo ========================================
echo.

REM Create all directories
echo Creating directories...
mkdir config 2>nul
mkdir apps 2>nul
mkdir apps\scraper 2>nul
mkdir apps\debate 2>nul
mkdir apps\sentiment 2>nul
mkdir apps\users 2>nul
mkdir apps\recommendations 2>nul
mkdir apps\feed 2>nul
mkdir apps\chatbot 2>nul
mkdir apps\speech 2>nul
mkdir static 2>nul
mkdir static\css 2>nul
mkdir static\js 2>nul
mkdir templates 2>nul

REM Create __init__.py files
echo Creating __init__.py files...
type nul > config\__init__.py
type nul > apps\__init__.py
type nul > apps\scraper\__init__.py
type nul > apps\debate\__init__.py
type nul > apps\sentiment\__init__.py
type nul > apps\users\__init__.py
type nul > apps\recommendations\__init__.py
type nul > apps\feed\__init__.py
type nul > apps\chatbot\__init__.py
type nul > apps\speech\__init__.py

REM Create docker-compose.yml
echo Creating docker-compose.yml...
(
echo version: '3.8'
echo.
echo services:
echo   # PostgreSQL with pgvector
echo   db:
echo     image: pgvector/pgvector:pg16
echo     container_name: lumen_postgres
echo     environment:
echo       POSTGRES_DB: lumen_news
echo       POSTGRES_USER: postgres
echo       POSTGRES_PASSWORD: postgres
echo     ports:
echo       - "5432:5432"
echo     volumes:
echo       - postgres_data:/var/lib/postgresql/data
echo     healthcheck:
echo       test: ["CMD-SHELL", "pg_isready -U postgres"]
echo       interval: 10s
echo       timeout: 5s
echo       retries: 5
echo.
echo   # Redis
echo   redis:
echo     image: redis:7-alpine
echo     container_name: lumen_redis
echo     ports:
echo       - "6379:6379"
echo     volumes:
echo       - redis_data:/data
echo     healthcheck:
echo       test: ["CMD", "redis-cli", "ping"]
echo       interval: 10s
echo       timeout: 5s
echo       retries: 5
echo.
echo   # Django Web Application
echo   web:
echo     build: .
echo     container_name: lumen_web
echo     command: python manage.py runserver 0.0.0.0:8000
echo     volumes:
echo       - .:/app
echo     ports:
echo       - "8000:8000"
echo     env_file:
echo       - .env
echo     environment:
echo       - DB_HOST=db
echo       - DB_PORT=5432
echo       - REDIS_URL=redis://redis:6379/0
echo       - CELERY_BROKER_URL=redis://redis:6379/0
echo       - CELERY_RESULT_BACKEND=redis://redis:6379/0
echo     depends_on:
echo       db:
echo         condition: service_healthy
echo       redis:
echo         condition: service_healthy
echo.
echo   # Celery Worker
echo   celery_worker:
echo     build: .
echo     container_name: lumen_celery_worker
echo     command: celery -A config worker -l info
echo     volumes:
echo       - .:/app
echo     env_file:
echo       - .env
echo     environment:
echo       - DB_HOST=db
echo       - DB_PORT=5432
echo       - REDIS_URL=redis://redis:6379/0
echo       - CELERY_BROKER_URL=redis://redis:6379/0
echo       - CELERY_RESULT_BACKEND=redis://redis:6379/0
echo     depends_on:
echo       db:
echo         condition: service_healthy
echo       redis:
echo         condition: service_healthy
echo.
echo   # Celery Beat
echo   celery_beat:
echo     build: .
echo     container_name: lumen_celery_beat
echo     command: celery -A config beat -l info
echo     volumes:
echo       - .:/app
echo     env_file:
echo       - .env
echo     environment:
echo       - DB_HOST=db
echo       - DB_PORT=5432
echo       - REDIS_URL=redis://redis:6379/0
echo       - CELERY_BROKER_URL=redis://redis:6379/0
echo       - CELERY_RESULT_BACKEND=redis://redis:6379/0
echo     depends_on:
echo       db:
echo         condition: service_healthy
echo       redis:
echo         condition: service_healthy
echo.
echo volumes:
echo   postgres_data:
echo   redis_data:
) > docker-compose.yml

REM Create Dockerfile
echo Creating Dockerfile...
(
echo FROM python:3.11-slim
echo.
echo ENV PYTHONUNBUFFERED=1
echo ENV PYTHONDONTWRITEBYTECODE=1
echo.
echo WORKDIR /app
echo.
echo RUN apt-get update ^&^& apt-get install -y \
echo     build-essential \
echo     libpq-dev \
echo     ffmpeg \
echo     ^&^& rm -rf /var/lib/apt/lists/*
echo.
echo COPY requirements.txt /app/
echo RUN pip install --upgrade pip
echo RUN pip install --no-cache-dir -r requirements.txt
echo.
echo COPY . /app/
echo.
echo EXPOSE 8000
echo.
echo CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
) > Dockerfile

REM Create .dockerignore
echo Creating .dockerignore...
(
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo venv/
echo env/
echo ENV/
echo .venv
echo *.log
echo db.sqlite3
echo media/
echo staticfiles/
echo .vscode/
echo .idea/
echo .DS_Store
echo Thumbs.db
echo .git/
) > .dockerignore

REM Create requirements.txt
echo Creating requirements.txt...
(
echo Django==5.0.0
echo python-decouple==3.8
echo psycopg2-binary==2.9.9
echo celery==5.3.4
echo redis==5.0.1
echo pgvector==0.2.4
echo torch==2.1.2
echo transformers==4.36.2
echo sentence-transformers==2.3.1
echo groq==0.4.1
echo feedparser==6.0.10
echo requests==2.31.0
echo beautifulsoup4==4.12.2
echo openai-whisper==20231117
echo soundfile==0.12.1
echo numpy==1.26.2
echo pandas==2.1.4
echo python-dateutil==2.8.2
) > requirements.txt

REM Create manage.py
echo Creating manage.py...
(
echo import os
echo import sys
echo.
echo if __name__ == '__main__':
echo     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'^)
echo     try:
echo         from django.core.management import execute_from_command_line
echo     except ImportError as exc:
echo         raise ImportError^(
echo             "Couldn't import Django."
echo         ^) from exc
echo     execute_from_command_line^(sys.argv^)
) > manage.py

REM Create config/__init__.py with celery import
echo Creating config/__init__.py...
(
echo from .celery import app as celery_app
echo.
echo __all__ = ^('celery_app',^)
) > config\__init__.py

REM Create config/settings.py
echo Creating config/settings.py...
(
echo import os
echo from pathlib import Path
echo from decouple import config
echo.
echo BASE_DIR = Path^(__file__^).resolve^(^).parent.parent
echo.
echo SECRET_KEY = config^('SECRET_KEY', default='dev-secret-key-change-in-production'^)
echo DEBUG = config^('DEBUG', default=True, cast=bool^)
echo ALLOWED_HOSTS = config^('ALLOWED_HOSTS', default='localhost,127.0.0.1'^).split^(','^)
echo.
echo INSTALLED_APPS = [
echo     'django.contrib.admin',
echo     'django.contrib.auth',
echo     'django.contrib.contenttypes',
echo     'django.contrib.sessions',
echo     'django.contrib.messages',
echo     'django.contrib.staticfiles',
echo     'apps.scraper',
echo     'apps.debate',
echo     'apps.sentiment',
echo     'apps.users',
echo     'apps.recommendations',
echo     'apps.feed',
echo     'apps.chatbot',
echo     'apps.speech',
echo ]
echo.
echo MIDDLEWARE = [
echo     'django.middleware.security.SecurityMiddleware',
echo     'django.contrib.sessions.middleware.SessionMiddleware',
echo     'django.middleware.common.CommonMiddleware',
echo     'django.middleware.csrf.CsrfViewMiddleware',
echo     'django.contrib.auth.middleware.AuthenticationMiddleware',
echo     'django.contrib.messages.middleware.MessageMiddleware',
echo     'django.middleware.clickjacking.XFrameOptionsMiddleware',
echo ]
echo.
echo ROOT_URLCONF = 'config.urls'
echo.
echo TEMPLATES = [
echo     {
echo         'BACKEND': 'django.template.backends.django.DjangoTemplates',
echo         'DIRS': [BASE_DIR / 'templates'],
echo         'APP_DIRS': True,
echo         'OPTIONS': {
echo             'context_processors': [
echo                 'django.template.context_processors.debug',
echo                 'django.template.context_processors.request',
echo                 'django.contrib.auth.context_processors.auth',
echo                 'django.contrib.messages.context_processors.messages',
echo             ],
echo         },
echo     },
echo ]
echo.
echo WSGI_APPLICATION = 'config.wsgi.application'
echo.
echo DATABASES = {
echo     'default': {
echo         'ENGINE': 'django.db.backends.postgresql',
echo         'NAME': config^('DB_NAME', default='lumen_news'^),
echo         'USER': config^('DB_USER', default='postgres'^),
echo         'PASSWORD': config^('DB_PASSWORD', default='postgres'^),
echo         'HOST': config^('DB_HOST', default='db'^),
echo         'PORT': config^('DB_PORT', default='5432'^),
echo     }
echo }
echo.
echo AUTH_PASSWORD_VALIDATORS = [
echo     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
echo     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
echo     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
echo     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
echo ]
echo.
echo LANGUAGE_CODE = 'en-us'
echo TIME_ZONE = 'UTC'
echo USE_I18N = True
echo USE_TZ = True
echo.
echo STATIC_URL = 'static/'
echo STATICFILES_DIRS = [BASE_DIR / 'static']
echo.
echo DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
echo.
echo CELERY_BROKER_URL = config^('CELERY_BROKER_URL', default='redis://redis:6379/0'^)
echo CELERY_RESULT_BACKEND = config^('CELERY_RESULT_BACKEND', default='redis://redis:6379/0'^)
echo CELERY_ACCEPT_CONTENT = ['json']
echo CELERY_TASK_SERIALIZER = 'json'
echo CELERY_RESULT_SERIALIZER = 'json'
echo CELERY_TIMEZONE = 'UTC'
) > config\settings.py

REM Create config/urls.py
echo Creating config/urls.py...
(
echo from django.contrib import admin
echo from django.urls import path
echo.
echo urlpatterns = [
echo     path^('admin/', admin.site.urls^),
echo ]
) > config\urls.py

REM Create config/wsgi.py
echo Creating config/wsgi.py...
(
echo import os
echo from django.core.wsgi import get_wsgi_application
echo.
echo os.environ.setdefault^('DJANGO_SETTINGS_MODULE', 'config.settings'^)
echo application = get_wsgi_application^(^)
) > config\wsgi.py

REM Create config/celery.py
echo Creating config/celery.py...
(
echo import os
echo from celery import Celery
echo.
echo os.environ.setdefault^('DJANGO_SETTINGS_MODULE', 'config.settings'^)
echo.
echo app = Celery^('lumen_news'^)
echo app.config_from_object^('django.conf:settings', namespace='CELERY'^)
echo app.autodiscover_tasks^(^)
) > config\celery.py

REM Create setup.bat
echo Creating setup.bat...
(
echo @echo off
echo echo ========================================
echo echo Lumen News - Docker Setup
echo echo ========================================
echo echo.
echo.
echo docker --version ^>nul 2^>^&1
echo if %%errorlevel%% neq 0 ^(
echo     echo [ERROR] Docker is not installed!
echo     pause
echo     exit /b 1
echo ^)
echo.
echo docker ps ^>nul 2^>^&1
echo if %%errorlevel%% neq 0 ^(
echo     echo [ERROR] Docker is not running!
echo     pause
echo     exit /b 1
echo ^)
echo.
echo if not exist .env ^(
echo     ^(
echo         echo SECRET_KEY=dev-secret-key-change-in-production
echo         echo DEBUG=True
echo         echo ALLOWED_HOSTS=localhost,127.0.0.1
echo         echo DB_NAME=lumen_news
echo         echo DB_USER=postgres
echo         echo DB_PASSWORD=postgres
echo         echo DB_HOST=db
echo         echo DB_PORT=5432
echo         echo REDIS_URL=redis://redis:6379/0
echo         echo CELERY_BROKER_URL=redis://redis:6379/0
echo         echo CELERY_RESULT_BACKEND=redis://redis:6379/0
echo         echo GROQ_API_KEY=your-groq-api-key-here
echo     ^) ^> .env
echo     echo .env created! Update GROQ_API_KEY before running!
echo     pause
echo ^)
echo.
echo docker-compose build
echo docker-compose up -d db redis
echo timeout /t 10 /nobreak ^>nul
echo docker-compose run --rm web python manage.py migrate
echo docker-compose run --rm web python manage.py createsuperuser
echo.
echo echo Setup complete! Run run.bat to start.
echo pause
) > setup.bat

REM Create run.bat
echo Creating run.bat...
(
echo @echo off
echo docker-compose up -d
echo echo.
echo echo Services started!
echo echo - Django: http://localhost:8000
echo echo - Admin: http://localhost:8000/admin
echo echo.
echo pause
echo docker-compose logs -f
) > run.bat

REM Create stop.bat
echo Creating stop.bat...
(
echo @echo off
echo docker-compose down
echo echo All services stopped!
echo pause
) > stop.bat

echo.
echo ========================================
echo Project structure created successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure Docker Desktop is installed and running
echo 2. Run: setup.bat
echo 3. Update .env with your GROQ_API_KEY
echo 4. Run: run.bat
echo.
pause