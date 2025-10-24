import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/vacunas/";


export const VacunasService = {
  // ✅ Obtener todas las vacunas
  async getAll() {
    const res = await axios.get(API_URL);
    return res.data;
  },

  // ✅ Registrar una nueva vacuna
  async create(vacuna) {
    const res = await axios.post(API_URL, vacuna);
    return res.data;
  },

  // ✅ Obtener detalle de una vacuna
  async getById(id) {
    const res = await axios.get(`${API_URL}${id}/`);
    return res.data;
  },

  // ✅ Actualizar una vacuna existente
  async update(id, data) {
    const res = await axios.put(`${API_URL}${id}/`, data);
    return res.data;
  },

  // ✅ Eliminar una vacuna
  async delete(id) {
    const res = await axios.delete(`${API_URL}${id}/`);
    return res.data;
  },
};
export default VacunasService;