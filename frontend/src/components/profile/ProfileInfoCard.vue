<template>
  <div class="bg-zinc-900 rounded-2xl shadow-2xl border border-zinc-800 p-6 hover:border-blue-500/50 transition-colors duration-300">
    <div class="flex items-center gap-3 mb-6">
      <User class="w-6 h-6 text-blue-400" />
      <h2 class="text-xl font-semibold text-white">Account Information</h2>
    </div>

    <div class="space-y-4">
      <!-- Username -->
      <div>
        <label class="text-sm text-gray-400 block flex items-center gap-2">
          <User class="w-4 h-4 text-blue-400/70" />
          <span>Username</span>
        </label>
        <p class="text-lg font-medium text-white mt-1">
          {{ user.username || '—' }}
        </p>
      </div>

      <!-- Email -->
      <div>
        <label class="text-sm text-gray-400 block flex items-center gap-2">
          <Mail class="w-4 h-4 text-blue-400/70" />
          <span>Email</span>
        </label>
        <p class="text-lg font-medium text-white mt-1">
          {{ user.email || '—' }}
        </p>
      </div>

      <!-- Status -->
      <div>
        <label class="text-sm text-gray-400 block flex items-center gap-2">
          <ShieldCheck class="w-4 h-4 text-blue-400/70" />
          <span>Status</span>
        </label>

        <span
          class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium mt-1"
          :class="
            user.is_active
              ? 'bg-green-500/20 text-green-300'
              : 'bg-red-500/20 text-red-300'
          "
        >
          <span
            class="w-2 h-2 rounded-full"
            :class="user.is_active ? 'bg-green-400' : 'bg-red-400'"
          ></span>

          {{ user.is_active ? 'Active' : 'Inactive' }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { User, Mail, ShieldCheck } from 'lucide-vue-next'

interface User {
  username?: string
  email?: string
  is_active?: boolean
}

defineProps<{
  user: User
}>()
</script>
