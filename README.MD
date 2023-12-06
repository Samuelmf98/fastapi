curso de fastapi

Crear entorno virtual: python3 -m venv nombre_venv

activa entorno virtual: source nombre_env/bin/activate

pip install fastapi uvicorn


ERROR:  [Errno 98] error while attempting to bind on address ('127.0.0.1', 8000): address already in use

solucion:

lsof -i :8000
kill -9 PID

Respuestas informativas (100–199),
Respuestas satisfactorias (200–299),
Redirecciones (300–399),
Errores de los clientes (400–499),
y errores de los servidores (500–599).

