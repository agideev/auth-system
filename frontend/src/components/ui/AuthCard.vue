<template>
  <div class="min-h-screen flex items-center justify-center bg-black p-4">
    <div class="w-full max-w-md">
      <div
        class="bg-zinc-900 rounded-2xl shadow-2xl border border-zinc-800 p-8 transition-all duration-300 hover:border-blue-500/50"
      >
        <!-- Logo -->
        <div class="flex justify-center mb-6">
          <div
            class="w-16 h-16 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-600/20"
          >
            <component :is="logo" class="w-8 h-8 text-white" />
          </div>
        </div>

        <!-- Títulos -->
        <h1 class="text-3xl font-bold text-center text-white mb-2">
          {{ title }}
        </h1>
        <p class="text-center text-gray-400 mb-8">
          {{ subtitle }}
        </p>

        <!-- Slot principal (formulário) -->
        <slot />

        <!-- Rodapé (link para login/registro) -->
        <p v-if="$slots.footer" class="text-center text-gray-400 text-sm mt-6">
          <slot name="footer" />
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  subtitle: string
  logo: any // Componente Lucide
}>()
</script>
