<template>
  <div class="lista-container">
    <h2>📋 Vacunas Registradas</h2>

    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Fabricante</th>
          <th>Dosis</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="v in vacunas" :key="v.id">
          <td>{{ v.id }}</td>
          <td>{{ v.nombre }}</td>
          <td>{{ v.fabricante }}</td>
          <td>{{ v.dosis }}</td>
          <td>
            <button @click="verDetalle(v.id)">🔍 Ver</button>
            <button @click="eliminarVacuna(v.id)">🗑️ Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="vacunas.length === 0">No hay vacunas registradas.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { VacunasService } from "@/utils/vacunas.service";

const vacunas = ref([]);
const router = useRouter();

const cargarVacunas = async () => {
  try {
    const data = await VacunasService.getAll();
    vacunas.value = data;
  } catch (error) {
    console.error("Error al obtener vacunas:", error);
  }
};

const verDetalle = (id) => {
  router.push(`/admin/vacunas/detalle/${id}`);
};

const eliminarVacuna = async (id) => {
  if (confirm("¿Seguro que deseas eliminar esta vacuna?")) {
    await VacunasService.delete(id);
    cargarVacunas();
  }
};

onMounted(() => cargarVacunas());
</script>

<style scoped>
.lista-container {
  padding: 2rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

th, td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

th {
  background-color: #003399;
  color: white;
}
button {
  margin: 0 5px;
  padding: 5px 10px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
button:hover {
  opacity: 0.8;
}
</style>
