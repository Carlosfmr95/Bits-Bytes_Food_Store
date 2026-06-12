# app/modules/pedidos/repository.py
"""
Repositorio para Pedido y tablas catálogo relacionadas.

"""
from sqlmodel import Session, select, func

from app.core.repository import BaseRepository
from app.modules.pedidos.models import (
    DetallePedido,
    EstadoPedido,
    FormaPago,
    Pedido,
)


class PedidoRepository(BaseRepository[Pedido]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, Pedido)

    # ── Listado general ───────────────────────────────────────────────────────

    def get_all_activos(self, offset: int = 0, limit: int = 20) -> list[Pedido]:
        """Todos los pedidos activos — para roles ADMIN / PEDIDOS ."""
        return list(self.session.exec(
            select(Pedido)
            .where(Pedido.deleted_at == None)           # noqa: E711
            .order_by(Pedido.created_at.desc())
            .offset(offset).limit(limit)
        ).all())

    def count_activos(self) -> int:
        return self.session.exec(
            select(func.count(Pedido.id)).where(Pedido.deleted_at == None)  # noqa: E711
        ).one()

    # ── Filtrado por usuario (CLIENT) ─────────────────────────────────────────

    def get_all_by_usuario(
        self, usuario_id: int, offset: int = 0, limit: int = 20
    ) -> list[Pedido]:
        """
        Pedidos activos de un usuario específico.
        Usado cuando el caller tiene solo rol CLIENT.
        """
        return list(self.session.exec(
            select(Pedido)
            .where(Pedido.deleted_at == None, Pedido.usuario_id == usuario_id)  # noqa: E711
            .order_by(Pedido.created_at.desc())
            .offset(offset).limit(limit)
        ).all())

    def count_by_usuario(self, usuario_id: int) -> int:
        return self.session.exec(
            select(func.count(Pedido.id))
            .where(Pedido.deleted_at == None, Pedido.usuario_id == usuario_id)  # noqa: E711
        ).one()

    # ── Detalles ──────────────────────────────────────────────────────────────

    def get_detalles(self, pedido_id: int) -> list[DetallePedido]:
        return list(self.session.exec(
            select(DetallePedido).where(DetallePedido.pedido_id == pedido_id)
        ).all())

    def add_detalle(self, detalle: DetallePedido) -> DetallePedido:
        self.session.add(detalle)
        self.session.flush()
        return detalle

    def delete_detalles(self, pedido_id: int) -> None:
        """Elimina todos los detalles de un pedido. Usado al editar pedido PENDIENTE."""
        from sqlalchemy import delete as sa_delete
        self.session.execute(
            sa_delete(DetallePedido).where(DetallePedido.pedido_id == pedido_id)
        )
        self.session.flush()


class CatalogoRepository:
    """Acceso de solo lectura a tablas catálogo (FormaPago, EstadoPedido)."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_forma_pago(self, codigo: str) -> FormaPago | None:
        return self.session.get(FormaPago, codigo)

    def get_estado(self, codigo: str) -> EstadoPedido | None:
        return self.session.get(EstadoPedido, codigo)

    def get_formas_pago_habilitadas(self) -> list[FormaPago]:
        return list(self.session.exec(
            select(FormaPago).where(FormaPago.habilitado == True)  
        ).all())
