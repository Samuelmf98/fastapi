from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional


app = FastAPI()
app.title = "Aplicacion de ventas"
app.version = "1.0.1"
ventas = [
    {"id": 1, "fecha": "01/12/2023", "tienda": "Tienda01", "importe": 100},
    {"id": 2, "fecha": "10/12/2023", "tienda": "Tienda02", "importe": 355},
    {"id": 3, "fecha": "10/12/2023", "tienda": "Tienda03", "importe": 355},
]


class Sales(BaseModel):  # creamos un modelo
    id: Optional[int]
    fecha: str
    tienda: str
    importe: float


# crear punto de entrada o endpoint
# ejecutar con uvicorn main:app --reload
# El reload es para si hacemos cambios los podamos ver sobre la marcha sin tener que cerrar y volver a ejecutar, simplemente refrescamos la pagina
# con --port 5000 cambiamos el puerto
# Direccion/docs  es para ver documentacion


@app.get("/", tags=["Inicio"])  # cambio de etiqueta en documentacion
def mensaje():
    return HTMLResponse("<h2>Titulo HTML desde FastAPI</h2>")


# direccion/ventas
@app.get("/ventas", tags=["Ventas"])
def dame_ventas():
    return ventas


# direccion/ventas/numero_personalizado
# Si el numero existe en el id de ventas me devuelve el diccionario entero,
# sino me devuelve una lista vacia
@app.get("/ventas/{id}", tags=["Ventas"])
def dame_ventas(id: int):
    for elem in ventas:
        if elem["id"] == id:
            return elem
    return "El valor introducido no existe"


# @app.get("/ventas", tags=["Ventas"])  # esta sobre escribiria la de arriba
# def dame_ventas_por_tienda(tienda: str):
#     return tienda


@app.get(
    "/ventas/", tags=["Ventas"]
)  # para evitarlo le ponemos una barra mas a /ventas
def dame_ventas_por_tienda(tienda: str, id: int):
    matching_ventas = []
    for elem in ventas:
        if elem["tienda"] == tienda or elem["id"] == id:
            matching_ventas.append(elem)

    if matching_ventas:
        return matching_ventas

    return "el valor introducido no existe"


# post


@app.post("/ventas", tags=["Ventas"])
def crea_ventas(venta: Sales):
    for sale in ventas:
        if sale.id == venta.id:
            return f"el elemento con id {venta.id} ya existe"

    ventas.append(venta)

    return ventas


# put
# modificar datos


@app.put("/ventas/{id}", tags=["Ventas"])
def actualiza_ventas(id: int, venta: Sales):
    for elem in ventas:
        if elem.id == id:
            elem.fecha = venta.fecha
            elem.tienda = venta.tienda
            elem.importe = venta.importe
    return ventas


# delete


@app.delete("/ventas{id}", tags=["Ventas"])
def borra_ventas(id: int):
    for elem in ventas:
        if elem.id == id:
            ventas.remove(elem)
    return ventas


# models
