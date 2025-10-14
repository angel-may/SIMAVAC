<template>
  <div class="dashboard">
    <Navbar />
    <div class="content">
      <h2>Panel del Tutor</h2>
      <p>Consulta y seguimiento de vacunación de tus hijos.</p>

      <div class="info">
        <div class="card">👶 Hijos registrados</div>
        <div class="card">📅 Próximas citas</div>
        <div class="card">💉 Vacunas pendientes</div>
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
  background: #eef3f8;
}

.content {
  flex: 1;
  padding: 2rem;
}

h2 {
  color: #001f4d;
}

.info {
  display: grid;
  margin-top: 2rem;
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
