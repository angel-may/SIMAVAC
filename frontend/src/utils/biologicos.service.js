// 📁 frontend/src/utils/biologicos.service.js
// Servicio centralizado para interactuar con el backend de Biológicos.
// Compatible con JWT y manejo automático de tokens (via api.js)

import api from "@/utils/api"

const BiologicosService = {
  // =====================================================
  // 🔹 Obtener todos los biológicos
  // =====================================================
  async getAll() {
    try {
      console.log("📡 Solicitando lista de biológicos...")
      const res = await api.get("/biologicos/")
      console.log("✅ Biológicos cargados correctamente:", res.data)
      return res.data
    } catch (err) {
      const status = err.response?.status
      const msg = err.response?.data?.detail || err.message
      console.error("❌ Error al obtener los biológicos:", msg)

      if (status === 401) {
        console.warn("⚠️ No autorizado o token no enviado. Revisa el interceptor o la sesión.")
        console.warn("Token actual:", localStorage.getItem("access"))
      }
      throw err
    }
  },

  // =====================================================
  // 🔹 Obtener un biológico por su ID
  // =====================================================
  async getById(id) {
    try {
      const res = await api.get(`/biologicos/${id}/`)
      console.log(`📦 Biológico ${id} obtenido correctamente.`)
      return res.data
    } catch (err) {
      console.error(`❌ Error al obtener el biológico ${id}:`, err.response?.data || err.message)
      throw err
    }
  },

  // =====================================================
  // 🔹 Crear un nuevo biológico
  // =====================================================
  async create(data) {
    try {
      console.log("🧬 Enviando registro de nuevo biológico...")
      const res = await api.post("/biologicos/", data)
      console.log("✅ Biológico registrado correctamente:", res.data)
      return res.data
    } catch (err) {
      const status = err.response?.status
      console.error("❌ Error al registrar el biológico:", err.response?.data || err.message)

      if (status === 401) {
        console.warn("⚠️ No autorizado. Verifica el token o la sesión.")
      }
      throw err
    }
  },

  // =====================================================
  // 🔹 Actualizar un biológico existente
  // =====================================================
  async update(id, data) {
    try {
      const res = await api.put(`/biologicos/${id}/`, data)
      console.log(`✅ Biológico ${id} actualizado correctamente.`)
      return res.data
    } catch (err) {
      console.error(`❌ Error al actualizar el biológico ${id}:`, err.response?.data || err.message)
      throw err
    }
  },

  // =====================================================
  // 🔹 Eliminar un biológico
  // =====================================================
  async delete(id) {
    try {
      const res = await api.delete(`/biologicos/${id}/`)
      console.log(`🗑️ Biológico ${id} eliminado correctamente.`)
      return res.data
    } catch (err) {
      console.error(`❌ Error al eliminar el biológico ${id}:`, err.response?.data || err.message)
      throw err
    }
  },

  // =====================================================
  // 🔹 Mover biológico a una unidad
  // =====================================================
  async moverAUnidad(id, payload) {
    try {
      const res = await api.post(`/biologicos/${id}/mover-a-unidad/`, payload)
      console.log("🚚 Movimiento registrado correctamente:", res.data)
      return res.data
    } catch (err) {
      console.error(
        `❌ Error al mover biológico ${id} a unidad:`,
        err.response?.data || err.message
      )
      throw err
    }
  },

  // =====================================================
  // 🔹 Obtener historial de movimientos
  // =====================================================
  async getMovimientos() {
    try {
      const res = await api.get("/almacen/")
      console.log(`📦 Movimientos cargados (${res.data.length} registros).`)
      return res.data
    } catch (err) {
      console.error("❌ Error al obtener movimientos del almacén:", err.response?.data || err.message)
      throw err
    }
  },
}

export default BiologicosService
