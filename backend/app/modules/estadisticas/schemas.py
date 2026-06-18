# app/modules/estadisticas/schemas.py
"""Schemas de solo lectura para el módulo de estadísticas."""
from datetime import date
from decimal import Decimal
from typing import Annotated, List, Optional

from pydantic import PlainSerializer
from sqlmodel import SQLModel

Monto = Annotated[
    Decimal,
    PlainSerializer(lambda v: float(v), return_type=float, when_used="json"),
]


class ProductoStockBajo(SQLModel):
    id: int
    nombre: str
    stock_cantidad: int


class ResumenResponse(SQLModel):
    ventas_hoy: Monto
    ventas_mes: Monto
    ticket_promedio: Monto
    pedidos_activos: int
    productos_stock_bajo: List[ProductoStockBajo]


class VentasPeriodoItem(SQLModel):
    periodo: str
    total_ventas: Monto
    cantidad_pedidos: int


class ProductoTopItem(SQLModel):
    producto_id: int
    nombre: str
    ingresos: Monto
    cantidad_vendida: int


class PedidosEstadoItem(SQLModel):
    estado_codigo: str
    cantidad: int


class IngresosItem(SQLModel):
    forma_pago_codigo: str
    total: Monto
    cantidad: int


class IngresosResponse(SQLModel):
    items: List[IngresosItem]
