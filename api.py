from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr, validator
import database as db
import helpers

class ModeloCliente(BaseModel):
    dni: constr(min_length=3, max_length=3)
    nombre: constr(min_length=2, max_length=30)
    apellido: constr(min_length=2, max_length=30)

class ModeloCrearCliente(ModeloCliente):
    @validator('dni')
    def validar_dni(cls, dni):
        if helpers.dni_valido(dni, db.Clientes.lista):
            return dni
        raise ValueError("Cliente ya existente o DNI incorrecto")


app = FastAPI(
    title="API del Gestor de clientes",
    description="Ofrece diferentes funciones para gestionar los clientes"
)

h = {"content-type": "text/plain; charset=utf-8"}

@app.get('/clientes/', tags=["Clientes"])
async def clientes():
    content= [cliente.to_dict() for cliente in db.Clientes.lista]
    return JSONResponse(content=content, headers=h)

@app.get('/clientes/buscar/{dni}', tags=["Clientes"])
async def clientes_buscar(dni: str):
    cliente = db.Clientes.buscar(dni=dni)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return JSONResponse(content=cliente.to_dict(), headers=h)


@app.post('/clientes/crear/', tags=["Clientes"])
async def cliente_crear(datos: ModeloCrearCliente):  #Se transfieren datos como si fuera un diccionario. urilizando la clase como contenido de la id "datos"
    cliente = db.Clientes.crear(datos.dni, datos.nombre, datos.apellido)
    if cliente:
        return JSONResponse(content=cliente.to_dict(), headers=h)
    raise HTTPException(status_code=404, detail="Cliente no creado")


@app.put('/clientes/actualziar/', tags=["Clientes"])
async def clientes_actualziar(datos: ModeloCliente):
    if db.Clientes.buscar(datos.dni):
        cliente = db.Clientes.modificar(datos.dni, datos.nombre, datos.apellido)
        if cliente:
            return JSONResponse(content=cliente.to_dict(), headers=h)
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.delete("/clientes/borrar/{dni}/", tags=["Clientes"])
async def clientes_borrar(dni: str):
    if db.Clientes.buscar(dni=dni):
        cliente = db.Clientes.borrar(dni=dni)
        return JSONResponse(content=cliente.to_dict(), headers=h)
    raise HTTPException(status_code=404)

print("Servidor de la API...")