<template>
  <AuthCard
    title="Create an account!"
    subtitle="Fill in the details below to get started"
    :logo="UserPlus"
  >
    <form @submit.prevent="handleRegister" class="space-y-5">
      <InputField
        v-model="form.username"
        label="Username"
        placeholder="Enter your username"
        type="text"
        :icon="User"
        :error="errors.username"
      />

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

      <CheckboxField
        v-model="form.acceptTerms"
        id="terms"
        label="I agree to the Terms of Service and Privacy Policy."
        :error="errors.acceptTerms"
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
        label="Create account"
        full-width
      />
    </form>

    <template #footer>
      Already have an account?
      <router-link
        to="/login"
        class="text-blue-400 font-medium hover:underline"
      >
        Sign in
      </router-link>
    </template>
  </AuthCard>
</template>


<script setup lang="ts">
import { ref, reactive } from 'vue'
import { UserPlus, User, Mail, Lock, CheckCircle, AlertCircle, Loader2 } from 'lucide-vue-next'
import api from '@/services/api'
import { authService } from '@/services/auth'
import formService from '@/services/formService'
import router from '@/router'

import AuthCard from '@/components/ui/AuthCard.vue'
import InputField from '@/components/ui/InputField.vue'
import FeedbackMessage from '@/components/ui/FeedbackMessage.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import CheckboxField from '@/components/ui/CheckboxField.vue'

interface RegisterForm {
  username: string
  email: string
  password: string
  acceptTerms: boolean
}

interface Errors {
  username?: string
  email?: string
  password?: string
  acceptTerms?: string
}

const form = reactive<RegisterForm>({
  username: '',
  email: '',
  password: '',
  acceptTerms: false,
})

const errors = reactive<Errors>({})

const loading = ref(false)

const feedback = reactive<{
  type: 'success' | 'error' | null
  message: string
}>({
  type: null,
  message: '',
})

const validateTerms = (): boolean => {
  if (!form.acceptTerms) {
    errors.acceptTerms = 'Você precisa aceitar os termos para continuar.'
    return false
  }

  delete errors.acceptTerms

  return true
}

const clearFieldError = (field: keyof Errors) => {
  delete errors[field]

  feedback.message = ''
  feedback.type = null
}

const handleRegister = async () => {
  formService.clearErrors(errors)
  feedback.message = ''
  feedback.type = null

  if (!validateTerms()) {
    return
  }

  loading.value = true

  try {
    const response = await api.post('/auth/register', {
      username: form.username,
      email: form.email,
      password: form.password,
    })

    const { access_token, message } = response.data

    authService.setToken(access_token)

    feedback.type = 'success'
    feedback.message = message || 'Cadastro realizado com sucesso!'

    setTimeout(() => {
      router.push('/profile')
    }, 500)

  } catch (error: any) {
    feedback.type = 'error'

    feedback.message = formService.handleError(
      error,
      errors,
      'Ocorreu um erro ao cadastrar. Tente novamente.'
    )

  } finally {
    loading.value = false
  }
}
</script>
