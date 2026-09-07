<template>
  <div class="min-h-screen bg-black text-white p-6">
    <div class="max-w-6xl mx-auto">
      <h1 class="text-3xl font-bold mb-8 text-blue-400 flex items-center gap-3">
        <User class="w-8 h-8" />
        My Profile
      </h1>

      <div class="flex flex-col gap-[10px]">
        <!-- Information Card -->
        <ProfileInfoCard
          :user="user"
          @edit="openEditModal"
        />

        <!-- Security Card -->
        <ProfileSecurityCard
          @changePassword="openChangePasswordModal"
          @editProfile="openEditModal"
          @logout="openLogoutDialog"
          @deleteAccount="openDeleteDialog"
        />
      </div>

      <!-- Modals -->
      <ModalEditProfile
        :isOpen="isEditModalOpen"
        :user="user"
        @close="isEditModalOpen = false"
        @updated="handleUserUpdated"
      />

      <ModalChangePassword
        :isOpen="isChangePasswordModalOpen"
        @close="isChangePasswordModalOpen = false"
      />

      <!-- Confirmation Dialog -->
      <ModalConfirm
        :isOpen="isConfirmDialogOpen"
        :title="dialogTitle"
        :message="dialogMessage"
        :confirm-text="dialogConfirmText"
        :confirm-type="dialogConfirmType"
        @confirm="handleDialogConfirm"
        @cancel="closeDialog"
      />
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { User } from 'lucide-vue-next'
import api from '@/services/api'
import { authService } from '@/services/auth'
import ProfileInfoCard from '@/components/profile/ProfileInfoCard.vue'
import ProfileSecurityCard from '@/components/profile/ProfileSecurityCard.vue'
import ModalEditProfile from '@/components/modals/ModalEditProfile.vue'
import ModalChangePassword from '@/components/modals/ModalChangePassword.vue'
import ModalConfirm from '@/components/modals/ModalConfirm.vue'
import axios from 'axios'

const router = useRouter()

interface User {
  id?: number
  username?: string
  email?: string
  is_active?: boolean
}

const user = ref<User>({})
const isEditModalOpen = ref(false)
const isChangePasswordModalOpen = ref(false)

// Dialog state
const isConfirmDialogOpen = ref(false)
const dialogTitle = ref('Confirmar')
const dialogMessage = ref('Tem certeza que deseja realizar esta ação?')
const dialogConfirmText = ref('Confirmar')
const dialogConfirmType = ref<'danger' | 'primary'>('primary')
let pendingAction: 'logout' | 'delete' | null = null

const fetchUser = async () => {
  try {
    const response = await api.get('/auth/me')
    if (response.data.success) {
      user.value = response.data.user
    }
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      authService.logout()
      router.push('/login')
    }
  }
}

onMounted(fetchUser)

const openEditModal = () => {
  isEditModalOpen.value = true
}

const openChangePasswordModal = () => {
  isChangePasswordModalOpen.value = true
}

const handleUserUpdated = (updatedUser: User) => {
  user.value = updatedUser
}

// Logout Dialog
const openLogoutDialog = () => {
  dialogTitle.value = 'Log Out'
  dialogMessage.value = 'Are you sure you want to end your current session?'
  dialogConfirmText.value = 'Log Out'
  dialogConfirmType.value = 'danger'
  pendingAction = 'logout'
  isConfirmDialogOpen.value = true
}

// Delete Dialog
const openDeleteDialog = () => {
  dialogTitle.value = 'Delete Account'
  dialogMessage.value = 'This action is irreversible. All your data will be permanently removed. Are you sure you want to continue?'
  dialogConfirmText.value = 'Delete Account'
  dialogConfirmType.value = 'danger'
  pendingAction = 'delete'
  isConfirmDialogOpen.value = true
}


const closeDialog = () => {
  isConfirmDialogOpen.value = false
  pendingAction = null
}

const handleDialogConfirm = async () => {
  if (pendingAction === 'logout') {
    authService.logout()
    router.push('/login')
  } else if (pendingAction === 'delete') {
    try {
      await api.delete('/auth/me')
      authService.logout()
      router.push('/login')
    } catch (error) {
      console.error('Erro ao deletar conta:', error)
      alert('Falha ao deletar conta. Tente novamente.')
    }
  }
  closeDialog()
}
</script>
