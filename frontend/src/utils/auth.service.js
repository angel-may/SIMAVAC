// 📁 frontend/src/utils/auth.service.js
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/auth/";

// ✅ Configuración base de Axios (para incluir tokens automáticamente)
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor: agrega token JWT si existe
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const AuthService = {
  // 🔹 Iniciar sesión
  async login(user, password) {
    try {
      const res = await api.post("login/", { user, password });
      const data = res.data;

      // 🧠 Compatibilidad doble:
      // Si el backend devuelve JWT (access / refresh), guardarlos
      if (data.access) {
        localStorage.setItem("access", data.access);
      }
      if (data.refresh) {
        localStorage.setItem("refresh", data.refresh);
      }

      return data;
    } catch (err) {
      console.error("Error en login:", err);
      if (err.response && err.response.data) {
        throw new Error(err.response.data.error || "Error al iniciar sesión");
      }
      throw new Error("No se pudo conectar con el servidor");
    }
  },

  // 🔹 Registrar usuario
  async register(data) {
    try {
      const res = await api.post("register/", data);
      return res.data;
    } catch (err) {
      console.error("Error en registro:", err);
      throw new Error(
        err.response?.data?.error || "No se pudo registrar el usuario"
      );
    }
  },

  // 🔹 Obtener roles (para selects)
  async getRoles() {
    try {
      const res = await api.get("roles/");
      return res.data;
    } catch (err) {
      throw new Error("No se pudieron obtener los roles");
    }
  },

  // 🔹 Refrescar token (si se usa SimpleJWT)
  async refreshToken() {
    const refresh = localStorage.getItem("refresh");
    if (!refresh) return null;

    try {
      const res = await axios.post(`${API_URL}token/refresh/`, { refresh });
      const newAccess = res.data.access;
      localStorage.setItem("access", newAccess);
      return newAccess;
    } catch (err) {
      console.warn("Token expirado o inválido");
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      return null;
    }
  },

  // 🔹 Cerrar sesión (limpieza de tokens)
  logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
  },
};
