<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
    @click.self="handleCancel"
  >
    <div class="bg-zinc-900 rounded-2xl p-6 max-w-md w-full border border-zinc-800 shadow-2xl animate-fade-in">
      <!-- Título -->
      <h3 class="text-xl font-semibold text-white mb-2">{{ title }}</h3>

      <!-- Mensagem -->
      <p class="text-gray-300 text-sm mb-6">{{ message }}</p>

      <!-- Botões -->
      <div class="flex gap-3 justify-end">
        <button
          @click="handleCancel"
          class="px-4 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-white text-sm font-medium transition-colors"
        >
          {{ cancelText }}
        </button>
        <button
          @click="handleConfirm"
          class="px-4 py-2 rounded-lg text-white text-sm font-medium transition-colors"
          :class="confirmClass"
        >
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    isOpen: boolean
    title?: string
    message?: string
    confirmText?: string
    cancelText?: string
    confirmType?: 'danger' | 'primary'
  }>(),
  {
    title: 'Confirmar',
    message: 'Tem certeza que deseja realizar esta ação?',
    confirmText: 'Confirmar',
    cancelText: 'Cancelar',
    confirmType: 'primary',
  }
)

const emit = defineEmits<{
  (e: 'confirm'): void
  (e: 'cancel'): void
}>()

const confirmClass = computed(() => {
  return props.confirmType === 'danger'
    ? 'bg-red-600 hover:bg-red-700'
    : 'bg-blue-600 hover:bg-blue-700'
})

const handleConfirm = () => {
  emit('confirm')
}

const handleCancel = () => {
  emit('cancel')
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
