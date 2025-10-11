import axios from 'axios'
import { useUserStore } from '../stores/user'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
})

let isRefreshing = false
let pending = []

api.interceptors.request.use((config) => {
  const store = useUserStore()
  if (store.access) config.headers.Authorization = `Bearer ${store.access}`
  return config
})

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const store = useUserStore()
    const original = error.config

    if (error.response && error.response.status === 401 && store.refresh && !original._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          pending.push({ resolve, reject })
        }).then((token) => {
          original.headers.Authorization = `Bearer ${token}`
          return api(original)
        })
      }
      original._retry = true
      isRefreshing = true
      try {
        const { data } = await axios.post('http://localhost:8000/api/core/auth/refresh/', {
          refresh: store.refresh,
        })
        store.setAccess(data.access)
        isRefreshing = false
        pending.forEach(p => p.resolve(data.access))
        pending = []
        original.headers.Authorization = `Bearer ${data.access}`
        return api(original)
      } catch (err) {
        isRefreshing = false
        pending.forEach(p => p.reject(err))
        pending = []
        store.logout()
        return Promise.reject(err)
      }
    }
    return Promise.reject(error)
  }
)

export default api
