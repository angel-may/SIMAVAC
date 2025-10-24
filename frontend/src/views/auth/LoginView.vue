<template>
  <div class="login-page">
    <div class="login-card">
      <h2 class="title">Iniciar sesión</h2>

      <form @submit.prevent="login">
        <div class="input-group">
          <label for="user">Usuario o correo</label>
          <input
            id="user"
            v-model.trim="user"
            placeholder="Correo, CURP o Usuario"
            required
          />
        </div>

        <div class="input-group">
          <label for="password">Contraseña</label>
          <input
            id="password"
            type="password"
            v-model.trim="password"
            placeholder="••••••••"
            required
          />
        </div>

        <button type="submit" class="btn" :disabled="loading">
          {{ loading ? "Entrando..." : "Iniciar sesión" }}
        </button>

        <p class="register-text">
          ¿No tienes cuenta?
          <router-link to="/register">Crear una cuenta</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useToast } from "vue-toastification"
import { AuthService } from "@/utils/auth.service"
import { useUserStore } from "@/stores/user"

const user = ref("")
const password = ref("")
const loading = ref(false)
const toast = useToast()
const router = useRouter()
const store = useUserStore()

const login = async () => {
  loading.value = true

  try {
    console.log("🧩 Enviando login con:", user.value, password.value)

    // 🔹 Llamada al backend
    const data = await AuthService.login(user.value, password.value)
    console.log("✅ Login exitoso, datos recibidos:", data)

    // 🔹 Guardar sesión (Pinia + localStorage)
    store.setSession(data)

    // 🔹 Mostrar bienvenida
    toast.success(`Bienvenido ${data.nombre} (${data.rol})`, {
      timeout: 2500,
      position: "top-right",
    })

    // 🔹 Redirección según el rol
    const rol = data.rol.toLowerCase().trim()
    let destino = "/"

    if (rol === "administrador") destino = "/admin"
    else if (rol === "doctor") destino = "/doctor"
    else if (rol === "enfermera") destino = "/enfermera"
    else if (rol === "tutor") destino = "/tutor"

    console.log("➡️ Redirigiendo a:", destino)
    await router.push(destino)
  } catch (error) {
    console.error("❌ Error en login:", error)
    toast.error(error.message || "Credenciales incorrectas")
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #001f4d, #004aad);
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 360px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.title {
  margin-bottom: 1.5rem;
  color: #001f4d;
}

.input-group {
  margin-bottom: 1rem;
  text-align: left;
}

.input-group label {
  display: block;
  margin-bottom: 0.3rem;
  color: #001f4d;
}

.input-group input {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
}

.btn {
  width: 100%;
  padding: 0.7rem;
  background: #001f4d;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn:hover {
  background: #003580;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-text {
  margin-top: 1rem;
}
</style>
