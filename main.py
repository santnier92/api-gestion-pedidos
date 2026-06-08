from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Plataforma de Gestión de Pedidos - DevOps AWS")

# Base de datos en memoria para el laboratorio
PEDIDOS = []
id_counter = 1

class PedidoCreate(BaseModel):
    cliente: str
    productos: List[str]
    cantidades: List[int]
    direccion_envio: str

class Pedido(PedidoCreate):
    id: int
    fecha_creacion: str
    estado: str  # Pendiente, En Proceso, Enviado, Entregado

@app.get("/")
def inicio():
    return {"mensaje": "Plataforma de Gestión de Pedidos Activa. Ve a /docs"}

# 1. Crear Pedido
@app.post("/pedidos", response_model=Pedido)
def crear_pedido(pedido: PedidoCreate):
    global id_counter
    nuevo_pedido = Pedido(
        id=id_counter,
        cliente=pedido.cliente,
        productos=pedido.productos,
        cantidades=pedido.cantidades,
        direccion_envio=pedido.direccion_envio,
        fecha_creacion=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        estado="Pendiente"
    )
    PEDIDOS.append(nuevo_pedido)
    id_counter += 1
    return nuevo_pedido

# 2. Visualizar Pedidos (Con filtro opcional por estado)
@app.get("/pedidos", response_model=List[Pedido])
def listar_pedidos(estado: Optional[str] = None):
    if estado:
        return [p for p in PEDIDOS if p.estado.lower() == estado.lower()]
    return PEDIDOS

# 3. Actualizar Estado del Pedido
@app.put("/pedidos/{pedido_id}/estado")
def actualizar_estado(pedido_id: int, nuevo_estado: str):
    estados_validos = ["Pendiente", "En Proceso", "Enviado", "Entregado"]
    if nuevo_estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Use: {estados_validos}")
    
    for pedido in PEDIDOS:
        if pedido.id == pedido_id:
            pedido.estado = nuevo_estado
            return {"mensaje": f"Pedido {pedido_id} actualizado a {nuevo_estado}", "pedido": pedido}
            
    raise HTTPException(status_code=404, detail="¡¡Pedido no encontrado!!")
