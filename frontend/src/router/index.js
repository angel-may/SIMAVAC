import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

import LoginView from '../views/auth/LoginView.vue'
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import EnfermeraDashboard from '../views/enfermera/EnfermeraDashboard.vue'
import AccesoDenegado from '../views/errores/AccesoDenegado.vue'

const routes = [
  { path: '/', name: 'login', component: LoginView, meta: { public: true } },
  { path: '/admin', name: 'admin', component: AdminDashboard, meta: { requiresAuth: true, roles: ['admin'] } },
  { path: '/enfermera', name: 'enfermera', component: EnfermeraDashboard, meta: { requiresAuth: true, roles: ['enfermera'] } },
  { path: '/denegado', name: 'denegado', component: AccesoDenegado, meta: { public: true } },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const store = useUserStore()
  if (to.meta.public) return true

  // si requiere auth y aún no tenemos user, intenta cargarlo con /me
  if (to.meta.requiresAuth && !store.isAuth) {
    if (store.access) {
      try { await store.fetchMe() } catch { store.logout() }
    }
  }
  if (to.meta.requiresAuth && !store.isAuth) return { name: 'login' }

  if (to.meta.roles?.length) {
    const ok = to.meta.roles.includes(store.rol)
    if (!ok) return { name: 'denegado' }
  }
  return true
})

export default router
