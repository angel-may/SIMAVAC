import { defineStore } from 'pinia'
import api from '../utils/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    access: localStorage.getItem('access') || null,
    refresh: localStorage.getItem('refresh') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null'),
  }),
  getters: {
    isAuth: (s) => !!s.access && !!s.user,
    rol: (s) => s.user?.rol || null,
  },
  actions: {
    setSession({ access, refresh, user }) {
      this.access = access
      this.refresh = refresh
      this.user = user
      localStorage.setItem('access', access)
      localStorage.setItem('refresh', refresh)
      localStorage.setItem('user', JSON.stringify(user))
    },
    setAccess(access) {
      this.access = access
      localStorage.setItem('access', access)
    },
    logout() {
      this.access = null
      this.refresh = null
      this.user = null
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      localStorage.removeItem('user')
    },
    async login(username, password) {
      const { data } = await api.post('/core/auth/login/', { username, password })
      this.setSession(data) // data: { access, refresh, user }
      return data.user
    },
    async fetchMe() {
      const { data } = await api.get('/core/auth/me/')
      this.user = data.user
      localStorage.setItem('user', JSON.stringify(this.user))
      return this.user
    },
  },
})
