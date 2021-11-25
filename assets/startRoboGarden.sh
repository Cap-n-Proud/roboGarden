cd NAS/Software/roboGarden/server/
source .venv/bin/activate
gunicorn wsgi:app  --bind 0.0.0.0:8000 --workers 1 --timeout 300000 --graceful-timeout 300000 --keep-alive 300000
