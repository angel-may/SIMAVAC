<template>
  <div v-if="biologico" class="card p-4">
    <h4>{{ biologico.nombre }}</h4>
    <p><strong>Lote:</strong> {{ biologico.lote }}</p>
    <p><strong>Fabricante:</strong> {{ biologico.fabricante }}</p>
    <p><strong>Caducidad:</strong> {{ biologico.fecha_caducidad }}</p>
    <p><strong>Cantidad disponible:</strong> {{ biologico.cantidad_disponible }}</p>
    <p><strong>Descripción:</strong> {{ biologico.descripcion || 'Sin descripción' }}</p>

    <hr />

    <h5>Movimientos en almacén</h5>
    <table class="table">
      <thead>
        <tr>
          <th>Tipo</th>
          <th>Unidad</th>
          <th>Cantidad</th>
          <th>Fecha</th>
          <th>Observaciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="mov in biologico.movimientos" :key="mov.idalmacen">
          <td>{{ mov.tipo }}</td>
          <td>{{ mov.idunidad || '-' }}</td>
          <td>{{ mov.cantidad }}</td>
          <td>{{ mov.fecha_registro }}</td>
          <td>{{ mov.observaciones }}</td>
        </tr>
      </tbody>
    </table>

    <router-link to="/admin/biologicos" class="btn btn-secondary mt-3">Volver</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import biologicosService from "@/utils/biologicos.service";

const route = useRoute();
const biologico = ref(null);

onMounted(async () => {
  const res = await biologicosService.getById(route.params.id);
  biologico.value = res.data;
});
</script>
