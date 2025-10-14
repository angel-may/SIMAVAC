<template>
  <nav class="navbar">
    <div class="navbar-left">
      <h1 class="logo">SIMAVAC</h1>
    </div>

    <div class="navbar-right">
      <span class="user-info">
        👤 {{ userName }} <small>({{ userRole }})</small>
      </span>
      <button class="logout-btn" @click="logout">Cerrar sesión</button>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const userName = ref("Usuario");
const userRole = ref("Rol");
const router = useRouter();

onMounted(() => {
  const userData = JSON.parse(localStorage.getItem("user"));
  if (userData) {
    userName.value = userData.nombre || "Usuario";
    userRole.value = userData.rol || "Rol";
  }
});

const logout = () => {
  localStorage.removeItem("user");
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  router.push("/");
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #001f4d;
  color: white;
  padding: 0.8rem 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.logo {
  font-size: 1.4rem;
  font-weight: bold;
  color: #ffffff;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  font-size: 0.95rem;
  font-weight: 500;
}

.logout-btn {
  background: #ff4757;
  color: white;
  border: none;
  padding: 0.5rem 0.9rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s;
}

.logout-btn:hover {
  background: #ff6b81;
}
</style>
