<template>
  <div class="form-container">
    <h2>🆕 Registrar Vacuna</h2>

    <form @submit.prevent="guardarVacuna">
      <label>Nombre:</label>
      <input v-model="vacuna.nombre" required />

      <label>Fabricante:</label>
      <input v-model="vacuna.fabricante" required />

      <label>Dosis:</label>
      <input type="number" v-model="vacuna.dosis" min="1" required />

      <label>Descripción:</label>
      <textarea v-model="vacuna.descripcion"></textarea>

      <button type="submit" class="btn-guardar">Guardar</button>
    </form>

    <p v-if="mensaje" class="mensaje">{{ mensaje }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { VacunasService } from "@/utils/vacunas.service";

const vacuna = ref({
  nombre: "",
  fabricante: "",
  dosis: "",
  descripcion: "",
});

const mensaje = ref("");

const guardarVacuna = async () => {
  try {
    await VacunasService.create(vacuna.value);
    mensaje.value = "✅ Vacuna registrada correctamente.";
    vacuna.value = { nombre: "", fabricante: "", dosis: "", descripcion: "" };
  } catch (err) {
    mensaje.value = "❌ Error al registrar la vacuna.";
    console.error(err);
  }
};
</script>

<style scoped>
.form-container {
  max-width: 500px;
  margin: 2rem auto;
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
label {
  font-weight: bold;
}
input,
textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}
.btn-guardar {
  background: #003399;
  color: white;
  padding: 0.8rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.btn-guardar:hover {
  background: #002266;
}
.mensaje {
  margin-top: 1rem;
  text-align: center;
  font-weight: bold;
}
</style>
