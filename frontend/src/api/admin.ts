// src/api/admin.ts
import { http } from './client'

export interface EstadoConteo {
  estado: string
  cantidad: number
}

export interface ProductoStockBajo {
  id: number
  nombre: string
  stock_cantidad: number
}

export interface DashboardStats {
  ventas_total: number
  cantidad_pedidos: number
  ticket_promedio: number
  pedidos_por_estado: EstadoConteo[]
  productos_stock_bajo: ProductoStockBajo[]
}

/** Métricas del panel de administración (solo ADMIN). */
export const getDashboardApi = () => http.get<DashboardStats>('/admin/dashboard').then(r => r.data)
