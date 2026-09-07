import axios from 'axios'
import { authService } from '@/services/auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Adiciona o token JWT automaticamente
api.interceptors.request.use(
  (config) => {
    const token = authService.getToken()

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Tratamento global de erros
api.interceptors.response.use(
  (response) => response,

  (error) => {
    console.error('Erro na requisição API:', error)

    // Token inválido ou expirado
    if (error.response?.status === 401) {
      authService.logout()
    }

    return Promise.reject(error)
  },
)

export default api
