// 📁 frontend/src/utils/auth.service.js
// Servicio centralizado para login, registro y gestión de tokens JWT

import api from "@/utils/api"  // ✅ Usa el mismo interceptor que biologicos.service.js
import axios from "axios"

const BASE_URL = "http://127.0.0.1:8000/api/auth/"

export const AuthService = {
  // =====================================================
  // 🔹 Iniciar sesión
  // =====================================================
  async login(user, password) {
    try {
      const res = await axios.post(`${BASE_URL}login/`, { user, password })
      const data = res.data

      // ✅ Guarda tokens localmente
      if (data.access) localStorage.setItem("access", data.access)
      if (data.refresh) localStorage.setItem("refresh", data.refresh)
      if (data.username) localStorage.setItem("user", JSON.stringify(data))

      console.log("🔐 Sesión iniciada correctamente:", data.username)
      return data
    } catch (err) {
      console.error("❌ Error en login:", err.response?.data || err.message)
      throw new Error(err.response?.data?.error || "Error al iniciar sesión")
    }
  },

  // =====================================================
  // 🔹 Registrar usuario (no requiere token)
  // =====================================================
  async register(data) {
    try {
      const res = await axios.post(`${BASE_URL}register/`, data)
      console.log("✅ Usuario registrado correctamente")
      return res.data
    } catch (err) {
      console.error("❌ Error en registro:", err.response?.data || err.message)
      throw new Error(
        err.response?.data?.error || "No se pudo registrar el usuario"
      )
    }
  },

  // =====================================================
  // 🔹 Obtener roles (público)
  // =====================================================
  async getRoles() {
    try {
      const res = await axios.get(`${BASE_URL}roles/`)
      return res.data
    } catch (err) {
      console.error("❌ No se pudieron obtener los roles:", err.response?.data || err.message)
      throw new Error("No se pudieron obtener los roles")
    }
  },

  // =====================================================
  // 🔹 Refrescar token (usando el endpoint correcto)
  // =====================================================
  async refreshToken() {
    const refresh = localStorage.getItem("refresh")
    if (!refresh) return null

    try {
      // ✅ Usa el endpoint correcto según el backend
      const res = await axios.post(`${BASE_URL}token/refresh/`, { refresh })
      const newAccess = res.data.access
      localStorage.setItem("access", newAccess)
      console.log("♻️ Token refrescado correctamente")
      return newAccess
    } catch (err) {
      console.warn("⚠️ Token expirado o inválido. Cerrando sesión.")
      localStorage.removeItem("access")
      localStorage.removeItem("refresh")
      localStorage.removeItem("user")
      return null
    }
  },

  // =====================================================
  // 🔹 Cerrar sesión (limpieza total)
  // =====================================================
  logout() {
    localStorage.removeItem("access")
    localStorage.removeItem("refresh")
    localStorage.removeItem("user")
    console.log("🚪 Sesión cerrada")
  },
}
