<template>
  <div>
    <div class="flex items-start gap-3 pt-2">
      <div class="relative flex items-center">
        <input
          :id="id"
          type="checkbox"
          :checked="modelValue"
          @change="$emit('update:modelValue', ($event.target as HTMLInputElement).checked)"
          class="peer sr-only"
        />

        <label
          :for="id"
          class="flex h-5 w-5 cursor-pointer items-center justify-center rounded-md
                 border bg-zinc-800 transition-all duration-200
                 peer-focus-visible:ring-2 peer-focus-visible:ring-blue-500/50
                 peer-checked:border-blue-500
                 peer-checked:bg-blue-600"
          :class="
            error
              ? 'border-red-500 peer-checked:bg-red-500'
              : 'border-zinc-600'
          "
        >
          <svg
            v-if="modelValue"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="3"
            class="h-3.5 w-3.5 text-white"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="m5 12 4 4L19 6"
            />
          </svg>
        </label>
      </div>

      <label
        :for="id"
        class="cursor-pointer select-none text-sm leading-5 text-gray-400"
      >
        <slot>
          Aceito os
          <a
            href="#"
            class="font-medium text-blue-400 transition hover:text-blue-300 hover:underline"
          >
            Termos de Serviço
          </a>
          e a
          <a
            href="#"
            class="font-medium text-blue-400 transition hover:text-blue-300 hover:underline"
          >
            Política de Privacidade
          </a>.
        </slot>
      </label>
    </div>

    <p
      v-if="error"
      class="mt-1.5 flex items-center gap-1 text-sm text-red-400"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        class="h-4 w-4 shrink-0"
      >
        <circle cx="12" cy="12" r="10" />
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M12 8v4m0 4h.01"
        />
      </svg>

      {{ error }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  modelValue: boolean
  id?: string
  error?: string
}>()

defineEmits<{
  (e: 'update:modelValue', value: boolean): void
}>()

const id = computed(
  () => props.id || `checkbox-${Math.random().toString(36).substring(2, 9)}`
)
</script>
