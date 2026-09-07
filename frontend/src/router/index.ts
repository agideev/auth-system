import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'

import { authService } from '../services/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/register',
      name: 'register',
      component: RegisterView,

      // Apenas usuários não autenticados
      meta: {
        requiresGuest: true,
      },
    },

    {
      path: '/login',
      name: 'login',
      component: LoginView,

      // Apenas usuários não autenticados
      meta: {
        requiresGuest: true,
      },
    },

    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,

      // Rota protegida
      meta: {
        requiresAuth: true,
      },
    },

    {
      path: '/',
      redirect: '/profile',
    },
  ],
})

// Proteção das rotas
router.beforeEach((to) => {
  const isAuthenticated = authService.isAuthenticated()

  // Usuário não autenticado tentando acessar uma rota protegida
  if (to.meta.requiresAuth && !isAuthenticated) {
    return {
      name: 'login',
      query: {
        redirect: to.fullPath,
      },
    }
  }

  // Usuário autenticado tentando acessar login ou registro
  if (to.meta.requiresGuest && isAuthenticated) {
    return {
      name: 'profile',
    }
  }

  return true
})

export default router
