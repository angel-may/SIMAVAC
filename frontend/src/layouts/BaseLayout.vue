<template>
  <div class="layout-container">
    <!-- 🔹 Header -->
    <header class="navbar">
      <h1 class="logo">{{ title }}</h1>
      <div class="user-info">
        <span>👤 {{ user?.nombre }} ({{ user?.rol }})</span>
        <button @click="logout" class="btn-logout">Cerrar sesión</button>
      </div>
    </header>

    <!-- 🔹 Contenedor principal -->
    <div class="layout-body">
      <!-- 🔸 Sidebar -->
      <aside class="sidebar">
        <h3>Menú</h3>
        <slot name="menu">
          <!-- Por defecto, el slot puede ser reemplazado -->
          <p>Menú no definido</p>
        </slot>
      </aside>

      <!-- 🔸 Contenido -->
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>

    <!-- 🔹 Footer -->
    <footer class="footer">
      <p>© 2025 SIMAVAC - Sistema Integral de Monitoreo de Vacunación</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const user = ref(JSON.parse(localStorage.getItem("user") || "{}"));
const props = defineProps({
  title: {
    type: String,
    default: "SIMAVAC - Panel",
  },
});

const logout = () => {
  localStorage.removeItem("user");
  router.push("/");
};
</script>

<style scoped>
.layout-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

/* ===== Navbar ===== */
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

/* ===== Layout principal ===== */
.layout-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* ===== Sidebar ===== */
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
.sidebar a.router-link-active {
  background: rgba(255, 255, 255, 0.3);
  font-weight: bold;
}

/* ===== Contenido principal ===== */
.main-content {
  flex: 1;
  padding: 2rem;
  background: #f4f6f9;
  overflow-y: auto;
}

/* ===== Footer ===== */
.footer {
  background: #001f4d;
  color: white;
  text-align: center;
  padding: 0.5rem;
  font-size: 0.85rem;
}

/* ===== Animación fade ===== */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
