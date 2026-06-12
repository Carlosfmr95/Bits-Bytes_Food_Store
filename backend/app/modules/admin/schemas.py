# app/modules/admin/schemas.py
"""Schemas del dashboard de administración (solo-lectura)."""
from decimal import Decimal
from typing import List

from sqlmodel import SQLModel


class EstadoConteo(SQLModel):
    estado: str
    cantidad: int


class ProductoStockBajo(SQLModel):
    id: int
    nombre: str
    stock_cantidad: int


class DashboardStats(SQLModel):
    """Métricas agregadas para el panel de administración."""
    ventas_total: Decimal
    cantidad_pedidos: int
    ticket_promedio: Decimal
    pedidos_por_estado: List[EstadoConteo]
    productos_stock_bajo: List[ProductoStockBajo]
