# app/modules/admin/service.py
"""
Service del dashboard de administración.

Agrega métricas de lectura para el panel: facturación, cantidad de pedidos,
distribución por estado y productos con stock bajo. Las consultas viven en
AdminRepository; aquí sólo está el cálculo de KPIs (sumas, ticket promedio).
"""
from decimal import Decimal

from sqlmodel import Session

from app.modules.admin.repository import AdminRepository
from app.modules.admin.schemas import (
    DashboardStats, EstadoConteo, ProductoStockBajo,
)

# Umbral por debajo del cual un producto se considera con stock bajo
UMBRAL_STOCK_BAJO = 10


class AdminService:
    def __init__(self, session: Session) -> None:
        self._repo = AdminRepository(session)

    def dashboard(self) -> DashboardStats:
        pedidos = list(self._repo.pedidos_facturables())
        cantidad = len(pedidos)
        ventas_total = sum((p.total for p in pedidos), Decimal("0"))
        ticket_promedio = (ventas_total / cantidad) if cantidad else Decimal("0")

        pedidos_por_estado = [
            EstadoConteo(estado=estado, cantidad=cant)
            for estado, cant in self._repo.conteo_por_estado()
        ]

        productos_stock_bajo = [
            ProductoStockBajo(id=p.id, nombre=p.nombre, stock_cantidad=p.stock_cantidad)
            for p in self._repo.productos_stock_bajo(UMBRAL_STOCK_BAJO)
        ]

        return DashboardStats(
            ventas_total=ventas_total,
            cantidad_pedidos=cantidad,
            ticket_promedio=ticket_promedio.quantize(Decimal("0.01")),
            pedidos_por_estado=pedidos_por_estado,
            productos_stock_bajo=productos_stock_bajo,
        )