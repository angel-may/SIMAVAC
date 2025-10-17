<template>
  <BaseLayout title="SIMAVAC - Administrador">
    <!-- Slot del menú lateral -->
    <template #menu>
      <router-link to="/admin" exact-active-class="active">🏠 Inicio</router-link>
      <router-link to="/admin/usuarios" exact-active-class="active">👥 Usuarios</router-link>
      <router-link to="/admin/vacunas/ver" exact-active-class="active">💉 Vacunas</router-link>
      <router-link to="/admin/campanias/ver" exact-active-class="active">📅 Campañas</router-link>
      <router-link to="/admin/reportes/vacunas" exact-active-class="active">📊 Reportes</router-link>
      <router-link to="/admin/configuracion" exact-active-class="active">⚙️ Configuración</router-link>
    </template>
  </BaseLayout>
</template>
<script setup>
import { useRouter } from "vue-router";
import { onMounted, ref } from "vue";
import BaseLayout from "@/layouts/BaseLayout.vue";
const router = useRouter();
const user = ref(JSON.parse(localStorage.getItem("user") || "{}"));

const logout = () => {
  localStorage.removeItem("user");
  router.push("/");
};

onMounted(() => {
  console.log("✅ Dashboard del Administrador cargado correctamente");
});
</script>

<style scoped>
/* ====== Layout general ====== */
.admin-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

/* ====== Navbar ====== */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: #002b80;
  color: white;
}

.logo {
  font-size: 1.2rem;
  font-weight: bold;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn-logout {
  background: #ff5555;
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s ease;
}

.btn-logout:hover {
  background: #ff3333;
}

/* ====== Layout interior ====== */
.layout {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* ====== Sidebar ====== */
.sidebar {
  width: 230px;
  background: #001f4d;
  color: white;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  gap: 0.5rem;
}

.sidebar h3 {
  margin-bottom: 1rem;
  font-size: 1rem;
  text-transform: uppercase;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  padding-bottom: 0.3rem;
}

.sidebar a {
  color: white;
  text-decoration: none;
  padding: 0.6rem 0.8rem;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.sidebar a:hover {
  background: rgba(255, 255, 255, 0.15);
}

.sidebar a.active {
  background: rgba(255, 255, 255, 0.3);
  font-weight: bold;
}

/* ====== Contenido principal ====== */
.main-content {
  flex: 1;
  padding: 2rem;
  background: #f4f6f9;
  overflow-y: auto;
}

/* ====== Bienvenida ====== */
.welcome {
  text-align: center;
  margin-top: 10%;
  color: #002b80;
}

/* ====== Transición ====== */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
