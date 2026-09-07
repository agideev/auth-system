<template>
  <div class="bg-zinc-900 rounded-2xl shadow-2xl border border-zinc-800 p-6 hover:border-blue-500/50 transition-colors duration-300">
    <div class="flex items-center gap-3 mb-6">
      <Shield class="w-6 h-6 text-blue-400" />
      <h2 class="text-xl font-semibold text-white">Security</h2>
    </div>

    <div class="space-y-3">
      <!-- Change Password -->
      <ActionButton
        icon="Key"
        color="blue"
        @click="emit('changePassword')"
      >
        <template #title>Change Password</template>
        <template #description>
          Change your password regularly to keep your account secure.
        </template>
      </ActionButton>

      <!-- Edit Profile -->
      <ActionButton
        icon="Edit"
        color="blue"
        @click="emit('editProfile')"
      >
        <template #title>Edit Profile</template>
        <template #description>
          Update your username and email address.
        </template>
      </ActionButton>

      <!-- Divider -->
      <div class="border-t border-zinc-700/50 my-2"></div>

      <!-- Logout -->
      <ActionButton
        icon="LogOut"
        color="red"
        @click="emit('logout')"
      >
        <template #title>Log Out</template>
        <template #description>
          Safely end your current session.
        </template>
      </ActionButton>

      <!-- Delete Account -->
      <ActionButton
        icon="Trash2"
        color="red"
        @click="emit('deleteAccount')"
      >
        <template #title>Delete Account</template>
        <template #description>
          Permanently delete your account and all associated data.
        </template>
      </ActionButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Shield } from 'lucide-vue-next'
import ActionButton from './ActionButton.vue' // ver abaixo

const emit = defineEmits<{
  (e: 'changePassword'): void
  (e: 'editProfile'): void
  (e: 'logout'): void
  (e: 'deleteAccount'): void
}>()
</script>
