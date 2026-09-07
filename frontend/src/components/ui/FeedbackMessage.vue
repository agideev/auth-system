<template>
  <div
    v-if="message"
    class="p-3 rounded-xl flex items-center gap-2 text-sm"
    :class="{
      'bg-green-500/10 text-green-400 border border-green-500/30': type === 'success',
      'bg-red-500/10 text-red-400 border border-red-500/30': type !== 'success',
    }"
  >
    <component :is="icon" class="w-5 h-5 flex-shrink-0" />
    <span>{{ message }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Check, AlertCircle } from 'lucide-vue-next'

const props = defineProps<{
  message: string
   type?: 'success' | 'error' | null
}>()

const icon = computed(() => {
  return props.type === 'success' ? Check : AlertCircle
})
</script>
