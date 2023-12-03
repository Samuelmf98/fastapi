curso de fastapi

Crear entorno virtual: python3 -m venv nombre_venv

activa entorno virtual: source nombre_env/bin/activate

pip install fastapi uvicorn


ERROR:    [Errno 98] error while attempting to bind on address ('127.0.0.1', 8000): address already in use

solucion:

lsof -i :8000
kill -9 PID

