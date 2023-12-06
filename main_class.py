from fastapi import FastAPI, Body, Path, Query
#Query es como Path pero para longitud de str
from fastapi.responses import HTMLResponse,JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_config import dame_token

#No veo cambios en la respuesta de la API al añadir List

app = FastAPI()
app.title = "Aplicacion de ventas"
app.version = "1.0.1"

ventas = [
    {"id": 1, "fecha": "01/12/2023", "tienda": "Tienda01", "importe": 100},
    {"id": 2, "fecha": "10/12/2023", "tienda": "Tienda02", "importe": 355},
    {"id": 3, "fecha": "10/12/2023", "tienda": "Tienda03", "importe": 355},
]

class Usuario(BaseModel):
    email:str
    clave:str

class Sales(BaseModel):  # creamos un modelo
    id: int =Field(ge=0,le=20) #mayor que cero y menor que 20
    #id: Optional[int]
    fecha: str
    tienda: str=Field(min_length=4,max_length=10)
    #tienda: str
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
@app.get("/ventas", tags=["Ventas"],response_model=List[Sales])
def dame_ventas()->List[Sales]: #No veo cambios el añadir List
    return JSONResponse(content=ventas) #para devolver un JSON


# direccion/ventas/numero_personalizado
# Si el numero existe en el id de ventas me devuelve el diccionario entero,
# sino me devuelve una lista vacia
@app.get("/ventas/{id}", tags=["Ventas"],response_model=List[Sales],status_code=200)
def dame_ventas(id: int=Path(ge=1,le=10)) -> Sales: #el ge y el le es para poner min y max permitidos
    for elem in ventas:
        if elem['id'] == id:
            return JSONResponse(content=elem,status_code=200)
    message = {"mensaje": f"El elemento con id {id} ya existe"}    
    return JSONResponse(content=message, status_code=404)


    
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


@app.post("/ventas", tags=["Ventas"],status_code=201)
def crea_ventas(venta: Sales):
    for sale in ventas:
        if sale['id'] == venta.id:
            return 'Ya existe un elemento con este id'
    ventas.append({"id": venta.id, "fecha": venta.fecha, "tienda": venta.tienda, "importe": venta.importe})
    return JSONResponse(content={'mensaje':'Venta registrada',
                                 'content':ventas},status_code=200)


# put
# modificar datos


@app.put("/ventas/{id}", tags=["Ventas"],status_code=201)
def actualiza_ventas(id: int, venta: Sales):
    for elem in ventas:
        if elem['id'] == id:
            elem['id']=venta.id
            elem['fecha'] = venta.fecha
            elem['tienda'] = venta.tienda
            elem['importe'] = venta.importe
    return JSONResponse(content={'mensaje':'Venta actualizada',
                                 'content':ventas},status_code=200)




# delete


@app.delete("/ventas{id}", tags=["Ventas"])
def borra_ventas(id: int):
    for elem in ventas:
        if elem['id'] == id:
            ventas.remove(elem)
    return JSONResponse(content={'mensaje':'Venta eliminada',
                                 'content':ventas})
        
             


#creamos ruta para login

@app.post('/login',tags=['Autenticacion'])
def login(usuario:Usuario):
    if usuario.email == 'samuel.mf1998@gmail.com' and usuario.clave == '1234':
        token:str=dame_token(usuario.dict())
        return JSONResponse(status_code=200,content=token)
    message='Error de autenticacion'
    return JSONResponse(content=message,status_code=401)