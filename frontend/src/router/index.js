import { createRouter, createWebHistory } from "vue-router";

// ======= Vistas principales =======
import LoginView from "@/views/auth/LoginView.vue";
import Register from "@/views/auth/Register.vue";
import AdminDashboard from "@/views/admin/Dashboard.vue";
import EnfermeraDashboard from "@/views/enfermera/Dashboard.vue";
import TutorDashboard from "@/views/tutor/Dashboard.vue";
import DoctorDashboard from "@/views/doctor/Dashboard.vue";

// ======= Módulos del Administrador =======
import Usuarios from "@/views/admin/usuarios.vue";
import Configuracion from "@/views/admin/configuracion.vue";
import RegistrarVacuna from "@/views/admin/vacunas/RegistrarVacuna.vue";
import VerVacunas from "@/views/admin/vacunas/VerVacunas.vue";
import RegistrarCampania from "@/views/admin/campanias/RegistrarCampanias.vue";
import VerCampanias from "@/views/admin/campanias/VerCampanias.vue";
import HistorialCampanias from "@/views/admin/campanias/HistorialCampanias.vue";
import ReportesVacunas from "@/views/admin/reportes/ReportesVacunas.vue";
import ReportesCampanias from "@/views/admin/reportes/ReportesCampanias.vue";

// ======= Errores =======
import AccesoDenegado from "@/views/errores/AccesoDenegado.vue";

const routes = [
  // 🔹 Página principal = Login
  { path: "/", name: "login", component: LoginView, meta: { public: true } },

  // 🔹 Registro
  { path: "/register", name: "register", component: Register, meta: { public: true } },

  // 🔹 ADMINISTRADOR con rutas hijas
  {
    path: "/admin",
    name: "admin",
    component: AdminDashboard,
    meta: { requiresAuth: true, roles: ["Administrador"] },
    children: [
      // --- Submódulos generales del administrador ---
      { path: "usuarios", component: Usuarios },
      { path: "configuracion", component: Configuracion },
      { path: "vacunas/registrar", component: RegistrarVacuna },
      { path: "vacunas/ver", component: VerVacunas },
      { path: "campanias/registrar", component: RegistrarCampania },
      { path: "campanias/ver", component: VerCampanias },
      { path: "campanias/historial", component: HistorialCampanias },
      { path: "reportes/vacunas", component: ReportesVacunas },
      { path: "reportes/campanias", component: ReportesCampanias },

      // --- Bloque original de vacunas ---
      {
        path: "",
        name: "menu-vacunas",
        component: () => import("@/views/admin/vacunas/MenuVacunas.vue"),
      },
      {
        path: "registrar",
        name: "registrar-vacuna",
        component: () => import("@/views/admin/vacunas/RegistrarVacuna.vue"),
      },
      {
        path: "ver",
        name: "ver-vacunas",
        component: () => import("@/views/admin/vacunas/VerVacunas.vue"),
      },
      {
        path: "detalle/:id",
        name: "detalle-vacuna",
        component: () => import("@/views/admin/vacunas/DetalleVacuna.vue"),
      },

      // --- 🔹 NUEVO BLOQUE DEL MÓDULO DE BIOLÓGICOS ---
      {
        path: "biologicos",
        component: () => import("@/views/admin/biologicos/MenuBiologico.vue"),
        children: [
          {
            path: "",
            name: "VerBiologicos",
            component: () => import("@/views/admin/biologicos/VerBiologicos.vue"),
          },
          {
            path: "registrar",
            name: "RegistrarBiologico",
            component: () => import("@/views/admin/biologicos/RegistrarBiologico.vue"),
          },
          {
            path: ":id",
            name: "DetalleBiologico",
            component: () => import("@/views/admin/biologicos/DetalleBiologico.vue"),
          },
        ],
      },
      // --- Fin del bloque de Biológicos ---
    ],
  },

  // 🔹 ENFERMERA
  {
    path: "/enfermera",
    name: "enfermera",
    component: EnfermeraDashboard,
    meta: { requiresAuth: true, roles: ["Enfermera"] },
  },

  // 🔹 DOCTOR
  {
    path: "/doctor",
    name: "doctor",
    component: DoctorDashboard,
    meta: { requiresAuth: true, roles: ["Doctor"] },
  },

  // 🔹 TUTOR
  {
    path: "/tutor",
    name: "tutor",
    component: TutorDashboard,
    meta: { requiresAuth: true, roles: ["Tutor"] },
  },

  // 🔹 Acceso denegado
  { path: "/denegado", name: "denegado", component: AccesoDenegado, meta: { public: true } },

  // 🔹 Redirección para rutas no encontradas
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

// ===========================================================
// 🔐 Protección global + herencia de meta del padre
// ===========================================================
const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  // 🧩 1. Heredar metadatos del padre si existen
  if (to.matched.length > 1) {
    const parent = to.matched[to.matched.length - 2];
    if (parent.meta.requiresAuth && !to.meta.requiresAuth) {
      to.meta.requiresAuth = parent.meta.requiresAuth;
      to.meta.roles = parent.meta.roles;
    }
  }

  // 🧩 2. Verificar si la ruta es pública
  if (to.meta.public) return next();

  // 🧩 3. Leer usuario de sesión
  let user = null;
  try {
    user = JSON.parse(localStorage.getItem("user"));
  } catch {
    user = null;
  }

  // 🧩 4. Si requiere login y no hay usuario → redirigir
  if (to.meta.requiresAuth && !user) {
    console.warn("🔒 Acceso bloqueado. No hay sesión activa.");
    return next({ name: "login" });
  }

  // 🧩 5. Verificar roles válidos
  if (to.meta.roles?.length && user) {
    const userRol = user.rol?.trim().toLowerCase();
    const allowedRoles = to.meta.roles.map((r) => r.trim().toLowerCase());
    if (!allowedRoles.includes(userRol)) {
      console.warn(`🚫 Rol "${userRol}" no autorizado para esta ruta.`);
      return next({ name: "denegado" });
    }
  }

  // 🧩 6. Si todo está correcto → continuar
  next();
});

export default router;
