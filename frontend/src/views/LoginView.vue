<template>
  <AuthCard
    title="Welcome back!"
    subtitle="Sign in to access your account"
    :logo="User"
  >
    <form
      @submit.prevent="handleLogin"
      class="space-y-5"
      autocomplete="off"
    >
      <InputField
        v-model="form.email"
        label="Email"
        placeholder="you@email.com"
        type="email"
        :icon="Mail"
        :error="errors.email"
      />

      <InputField
        v-model="form.password"
        label="Password"
        placeholder="Enter your password"
        type="password"
        :icon="Lock"
        :error="errors.password"
      />

      <FeedbackMessage
        v-if="feedback.message"
        :type="feedback.type"
        :message="feedback.message"
      />

      <BaseButton
        type="submit"
        variant="gradient"
        size="lg"
        :loading="loading"
        :disabled="loading"
        label="Sign in"
        full-width
      />
    </form>

    <template #footer>
      Don't have an account?
      <router-link
        to="/register"
        class="text-blue-400 font-medium hover:underline"
      >
        Create one now
      </router-link>
    </template>
  </AuthCard>
</template>


<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { LogIn, Mail, Lock, User } from 'lucide-vue-next'
import api from '@/services/api'
import { authService } from '@/services/auth'

// Componentes UI
import AuthCard from '@/components/ui/AuthCard.vue'
import InputField from '@/components/ui/InputField.vue'
import FeedbackMessage from '@/components/ui/FeedbackMessage.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import formService from '@/services/formService'

const router = useRouter()

// Formulário
const form = reactive({
  email: '',
  password: '',
})

const errors = reactive<{ email?: string; password?: string }>({})
const loading = ref(false)
const feedback = reactive<{ type: 'success' | 'error' | null; message: string }>({
  type: null,
  message: '',
})

// Se já estiver autenticado, redireciona para profile
onMounted(() => {
  if (authService.isAuthenticated()) {
    router.push('/profile')
  }
})


// Login
const handleLogin = async () => {

  formService.clearErrors(errors)
  feedback.message = ''
  feedback.type = null
  loading.value = true

  try {
    const response = await api.post('/auth/login', {
      email: form.email.trim(),
      password: form.password,
    })

    const data = response.data
    if (data.success && data.access_token) {
      authService.setToken(data.access_token)

      feedback.type = 'success'
      feedback.message = data.message || 'Login realizado com sucesso!'

      setTimeout(() => {
        router.push('/profile')
      }, 500)
    } else {
      throw new Error(data.message || 'Erro desconhecido')
    }
  } catch (error: any) {

    feedback.type = 'error'
    feedback.message = formService.handleError(
      error,
      errors,
      'Ocorreu um erro. Tente novamente.'
    )

  } finally {
    loading.value = false
  }
}
</script>
