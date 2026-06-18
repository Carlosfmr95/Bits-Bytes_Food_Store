// src/components/estadisticas/IngresosFormaPagoChart.tsx
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
} from 'recharts'
import type { IngresosItem } from '../../models/estadistica'

interface Props { data: IngresosItem[] }

const fmt = (n: number) =>
  n.toLocaleString('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 0 })

const COLORES = ['#3b82f6', '#22c55e', '#f59e0b', '#8b5cf6', '#ef4444']

export default function IngresosFormaPagoChart({ data }: Props) {
  if (!data.length) return <p className="text-sm text-gray-400 italic">Sin datos para el período.</p>
  const mapped = data.map(d => ({ ...d, total: Number(d.total) }))
  return (
    <ResponsiveContainer width="100%" height={Math.max(220, mapped.length * 56 + 48)}>
      <BarChart data={mapped} layout="vertical" margin={{ top: 8, right: 48, left: 8, bottom: 8 }}>
        <XAxis type="number" tickFormatter={fmt} tick={{ fontSize: 11 }} />
        <YAxis type="category" dataKey="forma_pago_codigo" tick={{ fontSize: 11 }} width={120} />
        <Tooltip formatter={(val, _name, props) => [`${fmt(Number(val))} · ${props.payload.cantidad} pedidos`, 'Total']} />
        <Bar dataKey="total" radius={[0, 6, 6, 0]}>
          {mapped.map((_e, i) => <Cell key={i} fill={COLORES[i % COLORES.length]} />)}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
