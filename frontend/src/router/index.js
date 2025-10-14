import { createRouter, createWebHistory } from "vue-router";

// 🟢 Vistas de autenticación
import LoginView from "@/views/auth/LoginView.vue";
import Register from "@/views/auth/Register.vue";

// 🟢 Dashboards principales
import AdminDashboard from "@/views/admin/Dashboard.vue";
import EnfermeraDashboard from "@/views/enfermera/Dashboard.vue";
import TutorDashboard from "@/views/tutor/Dashboard.vue";
import doctor from "@/views/doctor/Dashboard.vue"
// 🟢 Errores
import AccesoDenegado from "@/views/errores/AccesoDenegado.vue";

const routes = [
  // 🔹 Página principal = Login
  {
    path: "/",
    name: "login",
    component: LoginView,
    meta: { public: true },
  },

  // 🔹 Registro
  {
    path: "/register",
    name: "register",
    component: Register,
    meta: { public: true },
  },

  // 🔹 Dashboards por rol
  {
    path: "/admin",
    name: "admin",
    component: AdminDashboard,
    meta: { requiresAuth: true, roles: ["Administrador"] },
  },
  {
    path: "/enfermera",
    name: "enfermera",
    component: EnfermeraDashboard,
    meta: { requiresAuth: true, roles: ["Enfermera"] },
  },
  
  {
    path: "/tutor",
    name: "tutor",
    component: TutorDashboard,
    meta: { requiresAuth: true, roles: ["Tutor"] },
  },

  // 🔹 Acceso denegado
  {
    path: "/denegado",
    name: "denegado",
    component: AccesoDenegado,
    meta: { public: true },
  },

  // 🔹 Redirección para rutas no encontradas
  {
    path: "/:pathMatch(.*)*",
    redirect: "/",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

/* ===========================================================
   🔐 Protección básica temporal (sin store)
   =========================================================== */
router.beforeEach((to) => {
  const user = JSON.parse(localStorage.getItem("user"));

  // Si la ruta es pública (login, register, denegado)
  if (to.meta.public) return true;

  // Si requiere autenticación y no hay sesión guardada
  if (to.meta.requiresAuth && !user) {
    return { name: "login" };
  }

  // Si requiere rol específico
  if (to.meta.roles?.length && user) {
    const userRol = user.rol?.trim().toLowerCase();
    const allowedRoles = to.meta.roles.map((r) => r.trim().toLowerCase());
    if (!allowedRoles.includes(userRol)) {
      return { name: "denegado" };
    }
  }

  return true;
});

export default router;
