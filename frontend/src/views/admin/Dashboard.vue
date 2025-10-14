<template>
  <div class="dashboard">
    <Navbar />
    <div class="content">
      <h2>Panel del Administrador</h2>
      <p>Bienvenido al sistema de gestión de vacunación.</p>

      <div class="stats">
        <div class="card">👩‍⚕️ Personal de salud</div>
        <div class="card">👶 Niños registrados</div>
        <div class="card">💉 Vacunas aplicadas</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from "@/components/common/Navbar.vue";
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #f3f6fa;
}

.content {
  flex: 1;
  padding: 2rem;
}

h2 {
  color: #001f4d;
  margin-bottom: 0.5rem;
}

.stats {
  margin-top: 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}

.card {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  text-align: center;
  font-weight: 500;
  color: #001f4d;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
</style>
