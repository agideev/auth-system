<template>
  <!-- Overlay -->
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70"
    @click.self="close"
  >
    <!-- Modal Card -->
    <div
      class="bg-zinc-900 rounded-2xl shadow-2xl border border-blue-500/30 w-full max-w-md p-6 relative animate-fade-in"
    >
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center gap-3">
          <Key class="w-6 h-6 text-blue-400" />
          <h2 class="text-xl font-semibold text-white">Change Password</h2>
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
        <!-- Current Password -->
        <InputField
          v-model="form.current_password"
          label="Current password"
          placeholder="Enter your current password"
          type="password"
          :icon="Lock"
          :error="errors.current_password"
        />

        <!-- New Password -->
        <InputField
          v-model="form.new_password"
          label="New password"
          placeholder="New password (minimum 8 characters)"
          type="password"
          :icon="Lock"
          :error="errors.new_password"
        />

        <!-- Confirm New Password -->
        <InputField
          v-model="form.confirm_password"
          label="Confirm new password"
          placeholder="Confirm your new password"
          type="password"
          :icon="Lock"
          :error="errors.confirm_password"
        />

        <!-- Feedback -->
        <FeedbackMessage
          v-if="feedback.message"
          :message="feedback.message"
          :type="feedback.type"
        />

        <!-- Buttons -->
        <div class="flex gap-3 pt-2">
          <BaseButton
            variant="secondary"
            size="md"
            label="Cancel"
            @click="close"
            class="flex-1"
          />

          <BaseButton
            type="submit"
            variant="primary"
            size="md"
            :loading="loading"
            :disabled="loading"
            label="Change password"
            class="flex-1"
          />
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { Key, X, Lock } from 'lucide-vue-next'
import api from '@/services/api'
import { authService } from '@/services/auth'
import InputField from '@/components/ui/InputField.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import FeedbackMessage from '@/components/ui/FeedbackMessage.vue'
import formService from '@/services/formService'

// Props
const props = defineProps<{
  isOpen: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'close'): void
}>()

// Estado do formulário
const form = reactive({
  current_password: '',
  new_password: '',
  confirm_password: '',
})

const errors = reactive<{
  current_password?: string
  new_password?: string
  confirm_password?: string
}>({})

const loading = ref(false)
const feedback = reactive<{ type: 'success' | 'error'; message: string }>({
  type: 'success',
  message: '',
})

// Reset ao abrir
watch(
  () => props.isOpen,
  (open) => {
    if (open) {
      form.current_password = ''
      form.new_password = ''
      form.confirm_password = ''
      errors.current_password = undefined
      errors.new_password = undefined
      errors.confirm_password = undefined
      feedback.message = ''
      feedback.type = 'success'
    }
  },
  { immediate: true }
)

const close = () => {
  emit('close')
}

// Submissão
const handleSubmit = async () => {

  formService.clearErrors(errors)
  feedback.message = ''
  feedback.type = 'success'

  // if (!validate()) return

  loading.value = true

  try {
    const response = await api.put(
      '/auth/me/password',
      {
        current_password: form.current_password,
        new_password: form.new_password,
      },
      {
        headers: {
          Authorization: `Bearer ${authService.getToken()}`,
        },
      }
    )

    if (response.data.success) {
      feedback.type = 'success'
      feedback.message = response.data.message || 'Senha alterada com sucesso!'
      // Fecha o modal após 1.5s
      setTimeout(() => {
        close()
      }, 1500)
    } else {
      throw new Error(response.data.message || 'Erro desconhecido')
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
