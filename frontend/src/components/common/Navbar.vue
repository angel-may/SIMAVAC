<template>
  <header class="navbar">
    <div class="left">
      <strong>SIMAVAC</strong>
      <nav class="links" v-if="rol">
        <RouterLink v-if="rol === 'admin'" to="/admin">Panel admin</RouterLink>
        <RouterLink v-if="rol === 'enfermera'" to="/enfermera">Panel enfermera</RouterLink>
      </nav>
    </div>

    <div class="right" v-if="user">
      <span class="user">
        {{ user.username }} <small>({{ rol }})</small>
      </span>
      <button class="logout" @click="onLogout">Cerrar sesión</button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useUserStore } from '../../stores/user'

const store = useUserStore()
const router = useRouter()

const user = computed(() => store.user)
const rol  = computed(() => store.rol)

const onLogout = () => {
  store.logout()
  router.push({ name: 'login' })
}
</script>

<style scoped>
.navbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 16px; background: #0f172a; color: #fff;
}
.left { display: flex; align-items: center; gap: 18px; }
.links a { color: #93c5fd; margin-right: 12px; text-decoration: none; }
.links a.router-link-active { text-decoration: underline; }
.right { display: flex; align-items: center; gap: 12px; }
.user small { color: #cbd5e1; }
.logout {
  background: #ef4444; color: white; border: none; padding: 6px 10px;
  border-radius: 6px; cursor: pointer;
}
.logout:hover { background: #dc2626; }
</style>
