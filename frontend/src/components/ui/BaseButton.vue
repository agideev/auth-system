<template>
  <button
    @click="emit('click')"
    :type="type"
    :disabled="disabled || loading"
    class="inline-flex items-center justify-center gap-2 font-semibold rounded-xl transition-all duration-200 disabled:opacity-70 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-zinc-900"
    :class="[
      sizeClasses,
      variantClasses,
      { 'shadow-lg': variant === 'primary' || variant === 'gradient' }
    ]"
  >
    <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
    <component v-else-if="icon" :is="icon" class="w-5 h-5" />
    <span v-if="label || $slots.default">
      <slot>{{ label }}</slot>
    </span>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Loader2 } from 'lucide-vue-next'

type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'ghost' | 'gradient'
type ButtonSize = 'sm' | 'md' | 'lg'

const props = withDefaults(
  defineProps<{
    label?: string
    type?: 'button' | 'submit' | 'reset'
    variant?: ButtonVariant
    size?: ButtonSize
    icon?: any
    loading?: boolean
    disabled?: boolean
    fullWidth?: boolean
  }>(),
  {
    type: 'button',
    variant: 'primary',
    size: 'md',
    loading: false,
    disabled: false,
    fullWidth: false,
  }
)

// Classes de tamanho
const sizeClasses = computed(() => {
  const base = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
  }
  const width = props.fullWidth ? 'w-full' : ''
  return `${base[props.size]} ${width}`
})

// Classes de variante
const variantClasses = computed(() => {
  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white shadow-blue-600/20 hover:shadow-blue-600/40',
    secondary: 'bg-zinc-800 hover:bg-zinc-700 text-white border border-zinc-700',
    danger: 'bg-red-600 hover:bg-red-700 text-white shadow-red-600/20 hover:shadow-red-600/40',
    ghost: 'bg-transparent hover:bg-zinc-800/50 text-gray-300 hover:text-white',
    gradient: 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white shadow-blue-600/20 hover:shadow-blue-600/40',
  }
  return variants[props.variant]
})

const emit = defineEmits<{
  (e: 'click'): void
}>()
</script>
