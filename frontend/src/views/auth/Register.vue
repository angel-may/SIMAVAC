<template>
  <div class="register-container">
    <h2>Crear cuenta</h2>

    <form @submit.prevent="register">
      <!-- Datos personales -->
      <h3>Datos personales</h3>
      <div class="form-row">
        <input v-model="form.curp" placeholder="CURP" required />
        <input v-model="form.rfc" placeholder="RFC (opcional)" />
      </div>

      <div class="form-row">
        <input v-model="form.nom" placeholder="Nombre" required />
        <input v-model="form.app" placeholder="Apellido paterno" />
        <input v-model="form.apm" placeholder="Apellido materno" />
      </div>

      <div class="form-row">
        <select v-model="form.sexo" required>
          <option value="">Sexo</option>
          <option value="H">Masculino</option>
          <option value="M">Femenino</option>
        </select>

        <input
          type="date"
          v-model="form.fnac"
          placeholder="Fecha de nacimiento"
        />
      </div>

      <div class="form-row">
        <input v-model="form.tel" placeholder="Teléfono" />
        <input
          v-model="form.correo"
          type="email"
          placeholder="Correo electrónico"
          required
        />
      </div>

      <div class="form-row">
        <input
          v-model="form.tsangre"
          placeholder="Tipo de sangre (ej. O+, A-)"
        />
        <input
          v-model="form.direc"
          type="number"
          placeholder="ID dirección (opcional)"
        />
      </div>

      <div class="form-row">
        <select v-model="form.rol" required>
          <option value="">Seleccionar rol</option>
          <option
            v-for="r in roles"
            :key="r.idrol"
            :value="r.idrol"
          >
            {{ r.nombre }}
          </option>
        </select>
      </div>

      <!-- Credenciales -->
      <h3>Datos de usuario</h3>
      <div class="form-row">
        <input v-model="form.username" placeholder="Usuario" required />
        <input
          v-model="form.password"
          type="password"
          placeholder="Contraseña"
          required
        />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? "Registrando..." : "Crear cuenta" }}
      </button>
    </form>

    <p v-if="message" class="success">{{ message }}</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

// ============================================================
// 🌐 API base
// ============================================================
const API = "http://localhost:8000/api/";

// ============================================================
// 🧾 Estado reactivo
// ============================================================
const form = ref({
  curp: "",
  rfc: "",
  nom: "",
  app: "",
  apm: "",
  sexo: "",
  tel: "",
  correo: "",
  fnac: "",
  tsangre: "",
  direc: "",
  rol: "",
  username: "",
  password: "",
});

const roles = ref([]);
const message = ref("");
const error = ref("");
const loading = ref(false);

// ============================================================
// 🔹 Cargar roles al iniciar
// ============================================================
onMounted(async () => {
  try {
    const res = await axios.get(`${API}auth/roles/`);
    roles.value = res.data;
  } catch (err) {
    console.error("Error al cargar roles:", err);
    error.value = "No se pudieron cargar los roles.";
  }
});

// ============================================================
// 🔹 Enviar formulario de registro
// ============================================================
const register = async () => {
  message.value = "";
  error.value = "";
  loading.value = true;

  try {
    // Limpia RFC vacío (lo genera backend si no se manda)
    if (!form.value.rfc) delete form.value.rfc;

    const res = await axios.post(`${API}auth/register/`, form.value, {
      headers: { "Content-Type": "application/json" },
    });

    message.value = res.data.message || "Usuario registrado correctamente.";
    console.log("Registro exitoso:", res.data);

    // Limpia formulario
    Object.keys(form.value).forEach((k) => (form.value[k] = ""));
  } catch (err) {
    console.error("Error al registrar usuario:", err.response || err);
    error.value =
      err.response?.data?.error ||
      err.response?.data?.detail ||
      "Error al registrar usuario.";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  max-width: 650px;
  margin: 2rem auto;
  padding: 2rem;
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 1rem;
  color: #1e3a8a;
}

h3 {
  margin-top: 1.5rem;
  color: #374151;
}

.form-row {
  display: flex;
  gap: 10px;
  margin-bottom: 1rem;
}

input,
select {
  flex: 1;
  padding: 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  transition: border 0.2s;
}

input:focus,
select:focus {
  outline: none;
  border-color: #2563eb;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #2563eb;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s, transform 0.1s;
}

button:hover {
  background-color: #1d4ed8;
  transform: scale(1.02);
}

.success {
  color: green;
  text-align: center;
  margin-top: 1rem;
  font-weight: 500;
}

.error {
  color: red;
  text-align: center;
  margin-top: 1rem;
  font-weight: 500;
}
</style>
