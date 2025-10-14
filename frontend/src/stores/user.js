// 📁 frontend/src/stores/user.js
import { defineStore } from "pinia";
import { AuthService } from "@/utils/auth.service";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,         // Datos del usuario actual
    access: null,       // Token (si se usa JWT más adelante)
    isAuth: false,      // Estado de autenticación
  }),

  getters: {
    nombre: (state) => state.user?.nombre || "",
    rol: (state) => state.user?.rol || "",
    correo: (state) => state.user?.correo || "",
  },

  actions: {
    // 🔹 Iniciar sesión
    async login(user, password) {
      try {
        const data = await AuthService.login(user, password);
        this.user = data;
        this.isAuth = true;

        // Si más adelante manejas JWT, puedes guardar el token aquí
        if (data.access) this.access = data.access;

        // Guardar en localStorage para mantener sesión
        localStorage.setItem("user", JSON.stringify(data));

        return data;
      } catch (err) {
        this.logout();
        throw err;
      }
    },

    // 🔹 Obtener usuario actual (para auto-login)
    async fetchMe() {
      // Si hay datos previos en localStorage
      const localData = localStorage.getItem("user");
      if (localData) {
        this.user = JSON.parse(localData);
        this.isAuth = true;
        return this.user;
      } else {
        this.logout();
      }
    },

    // 🔹 Cerrar sesión
    logout() {
      this.user = null;
      this.access = null;
      this.isAuth = false;
      localStorage.removeItem("user");
    },
  },
});
