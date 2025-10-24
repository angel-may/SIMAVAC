<template>
  <div class="detalle-container" v-if="vacuna">
    <h2>🔍 Detalle de Vacuna</h2>
    <p><strong>Nombre:</strong> {{ vacuna.nombre }}</p>
    <p><strong>Fabricante:</strong> {{ vacuna.fabricante }}</p>
    <p><strong>Dosis:</strong> {{ vacuna.dosis }}</p>
    <p><strong>Descripción:</strong> {{ vacuna.descripcion }}</p>

    <button @click="volver">⬅️ Volver</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { VacunasService } from "@/utils/vacunas.service";

const route = useRoute();
const router = useRouter();
const vacuna = ref(null);

const cargarVacuna = async () => {
  const id = route.params.id;
  try {
    vacuna.value = await VacunasService.getById(id);
  } catch (err) {
    console.error("Error al obtener vacuna:", err);
  }
};

const volver = () => router.push("/admin/vacunas/ver");

onMounted(() => cargarVacuna());
</script>

<style scoped>
.detalle-container {
  max-width: 500px;
  margin: 2rem auto;
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
button {
  margin-top: 1rem;
  background: #003399;
  color: white;
  padding: 0.7rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
button:hover {
  background: #002266;
}
</style>
