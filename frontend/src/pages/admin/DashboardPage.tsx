// src/pages/admin/DashboardPage.tsx
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
} from 'recharts'
import { useQuery } from '@tanstack/react-query'
import { getDashboardApi } from '../../api/admin'
import { qk } from '../../queries/keys'

const COLORES_ESTADO: Record<string, string> = {
  PENDIENTE:  '#f59e0b',
  CONFIRMADO: '#3b82f6',
  EN_PREP:    '#8b5cf6',
  ENTREGADO:  '#22c55e',
  CANCELADO:  '#ef4444',
}

const formatoMoneda = (n: number) =>
  n.toLocaleString('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 0 })

export default function DashboardPage() {
  const dashboardQuery = useQuery({
    queryKey: qk.dashboard,
    queryFn: () => getDashboardApi(),
  })

  const stats = dashboardQuery.data ?? null
  const cargando = dashboardQuery.isLoading
  const error = dashboardQuery.error
    ? (dashboardQuery.error instanceof Error ? dashboardQuery.error.message : 'No se pudo cargar el dashboard.')
    : ''

  if (cargando) {
    return <div className="p-6 text-gray-500 dark:text-gray-400">Cargando métricas…</div>
  }
  if (error || !stats) {
    return <div className="p-6 text-red-600 dark:text-red-400">{error || 'Sin datos.'}</div>
  }

  const tarjetas = [
    { label: 'Facturación', valor: formatoMoneda(stats.ventas_total) },
    { label: 'Pedidos', valor: String(stats.cantidad_pedidos) },
    { label: 'Ticket promedio', valor: formatoMoneda(stats.ticket_promedio) },
  ]

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-100">Dashboard</h1>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {tarjetas.map((t) => (
          <div key={t.label} className="rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-5">
            <p className="text-sm text-gray-500 dark:text-gray-400">{t.label}</p>
            <p className="mt-1 text-2xl font-semibold text-gray-900 dark:text-gray-50">{t.valor}</p>
          </div>
        ))}
      </div>

      <div className="rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-5">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Pedidos por estado</h2>
        {stats.pedidos_por_estado.length === 0 ? (
          <p className="text-sm text-gray-400 italic">Todavía no hay pedidos.</p>
        ) : (
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={stats.pedidos_por_estado}>
              <XAxis dataKey="estado" tick={{ fontSize: 12 }} />
              <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="cantidad" radius={[6, 6, 0, 0]}>
                {stats.pedidos_por_estado.map((e) => (
                  <Cell key={e.estado} fill={COLORES_ESTADO[e.estado] ?? '#6b7280'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>

      <div className="rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-5">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Productos con stock bajo</h2>
        {stats.productos_stock_bajo.length === 0 ? (
          <p className="text-sm text-gray-400 italic">No hay productos con stock bajo.</p>
        ) : (
          <ul className="divide-y divide-gray-100 dark:divide-gray-700">
            {stats.productos_stock_bajo.map((p) => (
              <li key={p.id} className="flex items-center justify-between py-2">
                <span className="text-gray-700 dark:text-gray-200">{p.nombre}</span>
                <span className="text-sm font-medium text-amber-600 dark:text-amber-400">{p.stock_cantidad} u.</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
