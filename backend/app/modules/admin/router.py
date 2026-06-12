# app/modules/admin/router.py
"""Router del dashboard de administración. APIRouter sin prefix (se aplica en main.py)."""
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.modules.admin.schemas import DashboardStats
from app.modules.admin.service import AdminService
from app.modules.auth.dependencies import require_role

router = APIRouter()


def get_service(session: Session = Depends(get_session)) -> AdminService:
    return AdminService(session)


@router.get(
    "/dashboard",
    response_model=DashboardStats,
    summary="Métricas del panel de administración [ADMIN]",
)
def get_dashboard(
    svc: AdminService = Depends(get_service),
    _=Depends(require_role(["ADMIN"])),
) -> DashboardStats:
    """Facturación, cantidad de pedidos, distribución por estado y stock bajo."""
    return svc.dashboard()
