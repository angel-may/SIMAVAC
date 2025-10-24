<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h4>Listado de biológicos</h4>
      <button class="btn btn-primary" @click="loadBiologicos">Actualizar</button>
    </div>

    <table class="table table-striped">
      <thead class="table-dark">
        <tr>
          <th>Nombre</th>
          <th>Tipo</th>
          <th>Fabricante</th>
          <th>Lote</th>
          <th>Caducidad</th>
          <th>Cantidad</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="bio in biologicos" :key="bio.idbiologico">
          <td>{{ bio.nombre }}</td>
          <td>{{ bio.tipo || '-' }}</td>
          <td>{{ bio.fabricante || '-' }}</td>
          <td>{{ bio.lote || '-' }}</td>
          <td>{{ bio.fecha_caducidad || 'N/D' }}</td>
          <td>
            <span :class="cantidadClass(bio.cantidad_disponible)">
              {{ bio.cantidad_disponible }}
            </span>
          </td>
          <td>
            <span :class="estadoClass(bio.estado)">
              {{ bio.estado }}
            </span>
          </td>
          <td>
            <router-link :to="`/admin/biologicos/${bio.idbiologico}`" class="btn btn-sm btn-outline-info me-2">
              Ver
            </router-link>
            <button class="btn btn-sm btn-outline-danger" @click="eliminar(bio.idbiologico)">
              Eliminar
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import biologicosService from "@/utils/biologicos.service";

const biologicos = ref([]);

const loadBiologicos = async () => {
  const res = await biologicosService.getAll();
  biologicos.value = res.data;
};

const eliminar = async (id) => {
  if (confirm("¿Deseas eliminar este biológico?")) {
    await biologicosService.delete(id);
    loadBiologicos();
  }
};

const cantidadClass = (cantidad) =>
  cantidad <= 20 ? "text-danger fw-bold" : "text-success";

const estadoClass = (estado) =>
  estado === "activo" ? "badge bg-success" : "badge bg-secondary";

onMounted(loadBiologicos);
</script>
