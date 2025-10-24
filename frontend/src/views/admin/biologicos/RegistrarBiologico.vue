<template>
  <div class="card p-4 shadow-sm">
    <h4>Registrar nuevo biológico</h4>
    <form @submit.prevent="guardar">
      <div class="row g-3">
        <div class="col-md-6">
          <label class="form-label">Nombre</label>
          <input v-model="bio.nombre" class="form-control" required />
        </div>
        <div class="col-md-6">
          <label class="form-label">Tipo</label>
          <input v-model="bio.tipo" class="form-control" />
        </div>
        <div class="col-md-6">
          <label class="form-label">Fabricante</label>
          <input v-model="bio.fabricante" class="form-control" />
        </div>
        <div class="col-md-6">
          <label class="form-label">Lote</label>
          <input v-model="bio.lote" class="form-control" />
        </div>
        <div class="col-md-6">
          <label class="form-label">Fecha de caducidad</label>
          <input type="date" v-model="bio.fecha_caducidad" class="form-control" />
        </div>
        <div class="col-md-6">
          <label class="form-label">Cantidad total</label>
          <input type="number" v-model="bio.cantidad_total" class="form-control" required min="0" />
        </div>
        <div class="col-12">
          <label class="form-label">Descripción</label>
          <textarea v-model="bio.descripcion" class="form-control" rows="2"></textarea>
        </div>
      </div>

      <div class="mt-4">
        <button class="btn btn-success me-2" type="submit">Guardar</button>
        <router-link to="/admin/biologicos" class="btn btn-secondary">Cancelar</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import biologicosService from "@/utils/biologicos.service";

const router = useRouter();
const bio = ref({
  nombre: "",
  tipo: "",
  fabricante: "",
  lote: "",
  fecha_caducidad: "",
  cantidad_total: 0,
  descripcion: "",
});

const guardar = async () => {
  try {
    await biologicosService.create(bio.value);
    alert("✅ Biológico registrado correctamente");
    router.push("/admin/biologicos");
  } catch (err) {
    console.error("❌ Error al registrar el biológico:", err);
    if (err.response?.status === 401) {
      alert("Tu sesión ha expirado. Por favor, inicia sesión nuevamente.");
    } else {
      alert("Error al guardar el biológico. Revisa consola.");
    }
  }
};
console.log("🧬 RegistrarBiologico.vue cargado correctamente");
</script>
