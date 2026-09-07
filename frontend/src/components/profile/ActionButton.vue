<template>
  <button
    @click="$emit('click')"
    class="w-full px-5 py-3.5 bg-zinc-800/50 hover:bg-zinc-700/70 rounded-xl transition-all duration-200 flex items-center gap-4 text-white font-medium border border-zinc-700/50 hover:border-blue-500/30 group"
    :class="colorClass"
  >
    <div class="w-9 h-9 rounded-lg bg-current/10 flex items-center justify-center group-hover:bg-current/20 transition-colors flex-shrink-0"
      :style="{ color: iconColor }">
      <component :is="iconComponent" class="w-5 h-5" :class="iconRotateClass" />
    </div>
    <div class="flex flex-col items-start flex-1">
      <slot name="title" />
      <span class="text-xs text-gray-400 font-normal">
        <slot name="description" />
      </span>
    </div>
    <ChevronRight class="w-4 h-4 text-gray-500 ml-auto group-hover:text-gray-300 transition-colors flex-shrink-0" />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Key, Edit, LogOut, Trash2, ChevronRight } from 'lucide-vue-next'

const props = defineProps<{
  icon: 'Key' | 'Edit' | 'LogOut' | 'Trash2'
  color?: 'blue' | 'red'
}>()

const iconMap = {
  Key, Edit, LogOut, Trash2
}

const iconComponent = computed(() => iconMap[props.icon])
const iconColor = computed(() => props.color === 'red' ? '#ef4444' : '#3b82f6')
const iconRotateClass = computed(() => props.icon === 'Edit' ? 'transition-transform duration-300 group-hover:rotate-45' : '')

const colorClass = computed(() => {
  if (props.color === 'red') {
    return 'hover:bg-red-900/20 hover:border-red-500/30'
  }
  return 'hover:bg-zinc-700/70 hover:border-blue-500/30'
})

defineEmits<{
  (e: 'click'): void
}>()
</script>
