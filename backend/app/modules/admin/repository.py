# app/modules/admin/repository.py
"""
Repository del dashboard de administración.

Sólo lectura y cross-entity (Pedido + Producto): ejecuta las consultas y
devuelve filas/entidades crudas. El cálculo de KPIs (sumas, ticket promedio)
vive en el service. No hace commit ni levanta HTTPException.
"""
from typing import Sequence

from sqlmodel import Session, func, select

from app.modules.pedidos.models import Pedido
from app.modules.productos.models import Producto, TipoProducto


class AdminRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def pedidos_facturables(self) -> Sequence[Pedido]:
        """Pedidos vivos que computan facturación (excluye CANCELADO)."""
        return self.session.exec(
            select(Pedido).where(
                Pedido.deleted_at == None,  # noqa: E711
                Pedido.estado_codigo != "CANCELADO",
            )
        ).all()

    def conteo_por_estado(self) -> Sequence[tuple[str, int]]:
        """(estado_codigo, cantidad) agrupado por estado actual de cada pedido vivo."""
        return self.session.exec(
            select(Pedido.estado_codigo, func.count())
            .where(Pedido.deleted_at == None)  # noqa: E711
            .group_by(Pedido.estado_codigo)
        ).all()

    def productos_stock_bajo(self, umbral: int) -> Sequence[Producto]:
        """Productos terminados vivos con stock <= umbral, ordenados ascendente."""
        return self.session.exec(
            select(Producto)
            .where(
                Producto.deleted_at == None,  # noqa: E711
                Producto.tipo == TipoProducto.TERMINADO,
                Producto.stock_cantidad <= umbral,
            )
            .order_by(Producto.stock_cantidad)
        ).all()