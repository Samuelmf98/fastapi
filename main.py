from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app=FastAPI()
app.title = 'Aplicacion de ventas' 
app.version = '1.0.1'
ventas = [
    {   
        'id': 1,
        'fecha':'01/12/2023',
        'tienda' : 'Tienda01',
        'importe': 100
    },

    {
    
        'id': 2,
        'fecha':'10/12/2023',
        'tienda' : 'Tienda02',
        'importe': 355

    },

    {

        'id': 3,
        'fecha':'10/12/2023',
        'tienda' : 'Tienda02',
        'importe': 355
    }
]

#crear punto de entrada o endpoint
#ejecutar con uvicorn main:app --reload
#El reload es para si hacemos cambios los podamos ver sobre la marcha sin tener que cerrar y volver a ejecutar, simplemente refrescamos la pagina
#con --port 5000 cambiamos el puerto
#Direccion/docs  es para ver documentacion

@app.get('/',tags=['Inicio']) #cambio de etiqueta en documentacion
def mensaje():
    return HTMLResponse('<h2>Titulo HTML dedse FastAPI</h2>')

#direccion/ventas
@app.get('/ventas',tags=['Ventas'])  
def dame_ventas():
    return ventas

#direccion/ventas/numero_personalizado
#Si el numero existe en el id de ventas me devuelve el diccionario entero,
#sino me devuelve una lista vacia
@app.get('/ventas/{id}',tags=['Ventas'])
def dame_ventas(id:int):
    for elem in ventas:
        if elem['id'] == id:
            return elem
    return 'El valor introducido no existe'





