"""drop_es_opcional_from_producto_ingredientes

Revision ID: c9d0e1f2a3b4
Revises: b8c9d0e1f2a3
Create Date: 2026-06-18 00:01:00.000000

Elimina la columna producto_ingredientes.es_opcional.
La especificacion (UML v7) solo define es_removible para la personalizacion
del pedido (IDs de ingredientes removidos en DetallePedido.personalizacion).
es_opcional no esta en la spec ni se usa en ninguna capa.
"""
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c9d0e1f2a3b4"
down_revision: Union[str, None] = "b8c9d0e1f2a3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("producto_ingredientes", "es_opcional")


def downgrade() -> None:
    op.add_column(
        "producto_ingredientes",
        sa.Column(
            "es_opcional",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
    )
