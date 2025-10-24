<template>
  <div class="container py-4">
    <h2 class="mb-3">Gestión de Biológicos</h2>
    <router-link to="/admin/biologicos/registrar" class="btn btn-success mb-3">
      <i class="bi bi-plus-circle"></i> Registrar nuevo biológico
    </router-link>
    <!-- Aquí se mostrará VerBiologicos.vue, RegistrarBiologico.vue o DetalleBiologico.vue -->
    <router-view />
  </div>
</template>

<script setup>
console.log("🧬 MenuBiologicos.vue cargado correctamente");
</script>
