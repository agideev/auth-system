<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70"
    @click.self="close"
  >
    <div
      class="bg-zinc-900 rounded-2xl shadow-2xl border border-blue-500/30 w-full max-w-md p-6 relative animate-fade-in"
    >
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center gap-3">
          <Edit class="w-6 h-6 text-blue-400" />
          <h2 class="text-xl font-semibold text-white">Edit Profile</h2>
        </div>

        <button
          @click="close"
          class="text-gray-400 hover:text-white transition-colors"
          type="button"
        >
          <X class="w-6 h-6" />
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <InputField
          v-model="form.username"
          label="Username"
          placeholder="Your username"
          type="text"
          :icon="UserIcon"
          :error="errors.username"
        />

        <InputField
          v-model="form.email"
          label="Email"
          placeholder="you@email.com"
          type="email"
          :icon="MailIcon"
          :error="errors.email"
        />

        <FeedbackMessage
          v-if="feedback.message"
          :message="feedback.message"
          :type="feedback.type"
        />

        <div class="flex gap-3 pt-2">
          <BaseButton
            variant="secondary"
            label="Cancel"
            @click="close"
          />

          <BaseButton
            type="submit"
            variant="gradient"
            :loading="loading"
            :disabled="loading"
            label="Save"
            full-width
          />
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { Edit, X, User as UserIcon, Mail as MailIcon } from 'lucide-vue-next'
import api from '@/services/api'
import { authService } from '@/services/auth'
import InputField from '@/components/ui/InputField.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import FeedbackMessage from '@/components/ui/FeedbackMessage.vue'
import formService from '@/services/formService'

// Props
const props = defineProps<{
  isOpen: boolean
  user: {
    id?: number
    username?: string
    email?: string
    is_active?: boolean
  }
}>()

// Emits
const emit = defineEmits<{
  (e: 'close'): void
  (e: 'updated', user: any): void
}>()

// Estado do formulário
const form = reactive({
  username: '',
  email: '',
})

const errors = reactive<{ username?: string; email?: string }>({})
const loading = ref(false)
const feedback = reactive<{ type: 'success' | 'error'; message: string }>({
  type: 'success',
  message: '',
})

// Preenche o formulário quando o modal abre
watch(
  () => props.isOpen,
  (open) => {
    if (open && props.user) {
      form.username = props.user.username || ''
      form.email = props.user.email || ''
      errors.username = undefined
      errors.email = undefined
      feedback.message = ''
    }
  },
  { immediate: true }
)

const close = () => emit('close')

// Submissão
const handleSubmit = async () => {

  formService.clearErrors(errors)
  feedback.message = ''
  loading.value = true

  try {
    const response = await api.put(
      '/auth/me',
      {
        username: form.username.trim(),
        email: form.email.trim(),
      },
      {
        headers: {
          Authorization: `Bearer ${authService.getToken()}`,
        },
      }
    )

    const data = response.data
    if (data.success) {
      feedback.type = 'success'
      feedback.message = data.message || 'Perfil atualizado com sucesso!'
      emit('updated', data.user)
      setTimeout(() => close(), 1000)
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

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
.animate-fade-in {
  animation: fade-in 0.2s ease-out;
}
</style>
