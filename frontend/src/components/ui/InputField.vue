<template>
  <div>
    <!-- Label com ícone -->
    <label v-if="label" class="text-sm text-gray-400 block flex items-center gap-2 mb-1.5">
      <component :is="icon" class="w-4 h-4 text-blue-400/70" />
      <span>{{ label }}</span>
    </label>

    <div class="relative">
      <!-- Input -->
      <input
        :type="inputType"
        :value="modelValue"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        :placeholder="placeholder"
        class="w-full px-4 py-3 bg-zinc-800/50 border border-zinc-700 rounded-xl text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
        :class="{ 'border-red-500 ring-2 ring-red-500/50': error }"
      />

      <!-- Toggle de visibilidade para senha -->
      <button
        v-if="type === 'password'"
        type="button"
        @click="showPassword = !showPassword"
        class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition"
      >
        <Eye v-if="!showPassword" class="w-5 h-5" />
        <EyeOff v-else class="w-5 h-5" />
      </button>
    </div>

    <!-- Mensagem de erro -->
    <p v-if="error" class="text-red-400 text-sm mt-1">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Eye, EyeOff } from 'lucide-vue-next'

// Props
const props = defineProps<{
  modelValue: string
  label?: string
  placeholder?: string
  type?: 'text' | 'email' | 'password'
  icon?: any // Componente Lucide
  error?: string
}>()

// Emits
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

// Controle de visibilidade da senha
const showPassword = ref(false)

// Tipo de input real (text/password)
const inputType = computed(() => {
  if (props.type === 'password') {
    return showPassword.value ? 'text' : 'password'
  }
  return props.type || 'text'
})
</script>
