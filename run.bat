@echo off
docker-compose up -d
echo.
echo Services started!
echo - Django: http://localhost:8000
echo - Admin: http://localhost:8000/admin
echo.
pause
docker-compose logs -f
