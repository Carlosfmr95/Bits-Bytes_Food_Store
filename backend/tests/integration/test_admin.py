# tests/integration/test_admin.py
"""Tests del dashboard de administración."""
import pytest

pytestmark = pytest.mark.integration


def test_dashboard_admin_ok(client, admin_auth_headers):
    """ADMIN obtiene las métricas con la estructura esperada."""
    resp = client.get("/api/v1/admin/dashboard", headers=admin_auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "ventas_total" in data
    assert "cantidad_pedidos" in data
    assert "ticket_promedio" in data
    assert isinstance(data["pedidos_por_estado"], list)
    assert isinstance(data["productos_stock_bajo"], list)


def test_dashboard_cliente_forbidden(client, client_auth_headers):
    """Un CLIENT no puede ver el dashboard → 403."""
    resp = client.get("/api/v1/admin/dashboard", headers=client_auth_headers)
    assert resp.status_code == 403


def test_dashboard_sin_auth_401(client):
    resp = client.get("/api/v1/admin/dashboard")
    assert resp.status_code == 401
