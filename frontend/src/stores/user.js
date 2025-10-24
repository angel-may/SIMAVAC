// 📁 frontend/src/stores/user.js
// Gestión centralizada del usuario y sus tokens con Pinia

import { defineStore } from "pinia"

export const useUserStore = defineStore("user", {
  state: () => ({
    access: null,
    refresh: null,
    user: null, // objeto con username, nombre, rol, etc.
  }),

  actions: {
    // =====================================================
    // 🔹 Inicializar desde localStorage (auto-login)
    // =====================================================
    initFromStorage() {
      const access = localStorage.getItem("access")
      const refresh = localStorage.getItem("refresh")
      const user = localStorage.getItem("user")

      if (access && refresh) {
        this.access = access
        this.refresh = refresh
        this.user = user ? JSON.parse(user) : null
        console.log("🔄 Sesión restaurada desde localStorage:", this.user?.username)
      } else {
        console.warn("⚠️ No se encontró sesión guardada en localStorage.")
      }
    },

    // =====================================================
    // 🔹 Guardar sesión (al iniciar login)
    // =====================================================
    setSession(data) {
      this.access = data.access
      this.refresh = data.refresh
      this.user = {
        username: data.username,
        nombre: data.nombre,
        correo: data.correo,
        rol: data.rol,
        curp: data.curp,
      }

      localStorage.setItem("access", data.access)
      localStorage.setItem("refresh", data.refresh)
      localStorage.setItem("user", JSON.stringify(this.user))

      console.log("✅ Sesión guardada correctamente en store y localStorage.")
    },

    // =====================================================
    // 🔹 Actualizar access token (después de refresh)
    // =====================================================
    setAccess(newAccess) {
      this.access = newAccess
      localStorage.setItem("access", newAccess)
      console.log("♻️ Access token actualizado en store y localStorage.")
    },

    // =====================================================
    // 🔹 Cerrar sesión y limpiar datos
    // =====================================================
    logout() {
      this.access = null
      this.refresh = null
      this.user = null
      localStorage.removeItem("access")
      localStorage.removeItem("refresh")
      localStorage.removeItem("user")
      console.log("🚪 Sesión cerrada y datos limpiados.")
    },
  },
})
