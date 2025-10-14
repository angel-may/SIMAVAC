<template>
  <div class="dashboard">
    <Navbar />
    <div class="content">
      <h2>Panel de la Enfermera</h2>
      <p>Gestión de pacientes y registro de vacunas.</p>

      <div class="actions">
        <button class="btn">📋 Registrar vacunación</button>
        <button class="btn">👶 Ver pacientes</button>
        <button class="btn">💉 Historial de vacunas</button>
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
  background: #f8fafc;
}

.content {
  flex: 1;
  padding: 2rem;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn {
  background: #004aad;
  color: white;
  padding: 0.9rem 1.2rem;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

.btn:hover {
  background: #005be0;
}
</style>
