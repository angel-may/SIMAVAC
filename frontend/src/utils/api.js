// 📁 frontend/src/utils/api.js
import axios from "axios"
import { useUserStore } from "@/stores/user"

// 🔹 Instancia principal de Axios
const api = axios.create({
  baseURL: "http://localhost:8000/api",
  timeout: 10000,
})

// =======================================================
// 🧩 Variables para controlar el refresh
// =======================================================
let isRefreshing = false
let pending = []

// =======================================================
// 🧠 Interceptor de REQUEST
// =======================================================
api.interceptors.request.use((config) => {
  const store = useUserStore()
  const token = store?.access || localStorage.getItem("access")

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  } else {
    console.warn("⚠️ No se encontró token JWT para:", config.url)
  }

  return config
})

// =======================================================
// 🔄 Interceptor de RESPONSE (manejo automático del refresh)
// =======================================================
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const store = useUserStore()
    const original = error.config

    // Si es un error 401 y tenemos refresh disponible
    if (error.response?.status === 401 && !original._retry) {
      const refresh =
        store?.refresh || localStorage.getItem("refresh")

      if (!refresh) {
        console.warn("⚠️ No hay refresh token disponible.")
        store?.logout?.()
        return Promise.reject(error)
      }

      if (isRefreshing) {
        // Si ya hay un refresh en curso, esperar a que termine
        return new Promise((resolve, reject) => {
          pending.push({ resolve, reject })
        }).then((token) => {
          original.headers.Authorization = `Bearer ${token}`
          return api(original)
        })
      }

      original._retry = true
      isRefreshing = true

      try {
        console.log("♻️ Intentando refrescar el token...")
        const { data } = await axios.post(
          "http://localhost:8000/api/auth/token/refresh/",
          { refresh }
        )

        if (!data.access) {
          throw new Error("No se devolvió nuevo access token")
        }

        // ✅ Guarda y propaga el nuevo access token
        store?.setAccess?.(data.access)
        localStorage.setItem("access", data.access)

        isRefreshing = false
        pending.forEach((p) => p.resolve(data.access))
        pending = []

        // Reintenta la petición original
        original.headers.Authorization = `Bearer ${data.access}`
        return api(original)
      } catch (err) {
        console.error("⚠️ Error al refrescar token:", err.response?.data || err.message)
        isRefreshing = false
        pending.forEach((p) => p.reject(err))
        pending = []
        store?.logout?.()
        localStorage.removeItem("access")
        localStorage.removeItem("refresh")
        return Promise.reject(new Error("Refresh token inválido o expirado."))
      }
    }

    return Promise.reject(error)
  }
)

export default api
