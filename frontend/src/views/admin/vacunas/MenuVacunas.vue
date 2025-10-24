<template>
  <div class="menu-container">
    <h2>💉 Módulo de Vacunas</h2>
    <p>Selecciona una opción para continuar:</p>

    <div class="menu-cards">
      <div class="card" @click="goTo('registrar')">
        <h3>🆕 Registrar Vacuna</h3>
        <p>Agrega una nueva vacuna al sistema.</p>
      </div>

      <div class="card" @click="goTo('ver')">
        <h3>📋 Ver Vacunas</h3>
        <p>Consulta el listado completo de vacunas registradas.</p>
      </div>

      <div class="card" @click="goTo('reportes')">
        <h3>📊 Reportes</h3>
        <p>Visualiza estadísticas y reportes de vacunación.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
const router = useRouter();

const goTo = (section) => {
  const routes = {
    registrar: "/admin/vacunas/registrar",
    ver: "/admin/vacunas/ver",
    reportes: "/admin/reportes/vacunas",
  };
  router.push(routes[section]);
};
</script>

<style scoped>
.menu-container {
  text-align: center;
  padding: 2rem;
}

.menu-cards {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
  margin-top: 2rem;
}

.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 280px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

h3 {
  color: #003399;
}
</style>
