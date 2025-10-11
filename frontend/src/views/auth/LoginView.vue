<template>
  <div class="min-h-screen grid place-items-center bg-gray-50 p-6">
    <div class="w-full max-w-sm bg-white shadow rounded p-6">
      <h1 class="text-xl font-semibold mb-4">Iniciar sesión</h1>

      <form @submit.prevent="onSubmit" class="space-y-3">
        <div>
          <label class="block text-sm">Usuario</label>
          <input v-model="form.username" class="border rounded w-full p-2" autocomplete="username" required />
        </div>
        <div>
          <label class="block text-sm">Contraseña</label>
          <input type="password" v-model="form.password" class="border rounded w-full p-2"
                 autocomplete="current-password" required />
        </div>
        <button :disabled="loading" class="w-full py-2 rounded bg-blue-600 text-white">
          {{ loading ? 'Ingresando...' : 'Entrar' }}
        </button>
        <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'

const router = useRouter()
const store = useUserStore()

const form = reactive({ username: '', password: '' })
const loading = ref(false)
const error = ref('')

const onSubmit = async () => {
  error.value = ''
  loading.value = true
  try {
    const user = await store.login(form.username, form.password)
    if (user.rol === 'admin') router.push({ name: 'admin' })
    else if (user.rol === 'enfermera') router.push({ name: 'enfermera' })
    else router.push({ name: 'denegado' })
  } catch (e) {
    error.value = e?.response?.data?.detail || e?.response?.data?.message || 'Credenciales inválidas'
  } finally {
    loading.value = false
  }
}
</script>
