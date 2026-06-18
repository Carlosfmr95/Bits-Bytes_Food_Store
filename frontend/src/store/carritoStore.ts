// src/store/carritoStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { ItemCarrito } from '../models/carrito'
import type { Producto } from '../models/producto'

export function lineaKey(producto_id: number, personalizacion: number[]): string {
  return `${producto_id}:${[...personalizacion].sort((a, b) => a - b).join(',')}`
}

interface AgregarOpciones {
  cantidad?: number
  personalizacion?: number[]
  sin_ingredientes?: string[]
}

interface CarritoState {
  items: ItemCarrito[]
  agregarItem: (producto: Producto, opciones?: AgregarOpciones) => void
  quitarItem: (key: string) => void
  cambiarCantidad: (key: string, cantidad: number) => void
  vaciarCarrito: () => void
}

export const useCarritoStore = create<CarritoState>()(
  // persist sincroniza los items al localStorage bajo la clave "carrito".
  persist(
    (set) => ({
      items: [],

      /** Suma cantidad si la misma combinación producto+personalización ya está; si no, agrega línea nueva. */
      agregarItem: (producto, opciones = {}) =>
        set((state) => {
          const cantidad = opciones.cantidad ?? 1
          const personalizacion = opciones.personalizacion ?? []
          const sin_ingredientes = opciones.sin_ingredientes ?? []
          const key = lineaKey(producto.id, personalizacion)
          const existente = state.items.find((i) => lineaKey(i.producto_id, i.personalizacion) === key)
          if (existente) {
            return {
              items: state.items.map((i) =>
                lineaKey(i.producto_id, i.personalizacion) === key
                  ? { ...i, cantidad: i.cantidad + cantidad }
                  : i,
              ),
            }
          }
          return {
            items: [
              ...state.items,
              {
                producto_id: producto.id,
                nombre: producto.nombre,
                precio_base: producto.precio_base,
                cantidad,
                imagen_url: producto.imagenes_url?.[0] ?? null,
                personalizacion,
                sin_ingredientes,
              },
            ],
          }
        }),

      /** Quita una línea del carrito por su clave. */
      quitarItem: (key) =>
        set((state) => ({ items: state.items.filter((i) => lineaKey(i.producto_id, i.personalizacion) !== key) })),

      /** Fija la cantidad de una línea; si baja a 0 o menos, la quita. */
      cambiarCantidad: (key, cantidad) =>
        set((state) => {
          if (cantidad <= 0) {
            return { items: state.items.filter((i) => lineaKey(i.producto_id, i.personalizacion) !== key) }
          }
          return {
            items: state.items.map((i) =>
              lineaKey(i.producto_id, i.personalizacion) === key ? { ...i, cantidad } : i,
            ),
          }
        }),

      /** Vacía el carrito por completo. */
      vaciarCarrito: () => set({ items: [] }),
    }),
    { name: 'carrito' },
  ),
)

/**
 * Hook de conveniencia: expone los items, las acciones y los totales derivados,
 * conservando la API que consumían los componentes desde CarritoContext.
 */
export function useCarrito() {
  const items = useCarritoStore((s) => s.items)
  const agregarItem = useCarritoStore((s) => s.agregarItem)
  const quitarItem = useCarritoStore((s) => s.quitarItem)
  const cambiarCantidad = useCarritoStore((s) => s.cambiarCantidad)
  const vaciarCarrito = useCarritoStore((s) => s.vaciarCarrito)

  const totalItems = items.reduce((acc, i) => acc + i.cantidad, 0)
  const totalPrecio = items.reduce((acc, i) => acc + i.precio_base * i.cantidad, 0)

  return { items, totalItems, totalPrecio, agregarItem, quitarItem, cambiarCantidad, vaciarCarrito }
}
