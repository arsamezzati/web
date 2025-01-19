// components/AuthModal.vue
<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
      <div class="flex justify-between mb-4">
        <h2 class="text-xl font-bold">{{ isLogin ? 'Login' : 'Sign Up' }}</h2>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <div class="flex gap-4 mb-4">
        <button 
          @click="isLogin = true"
          :class="['flex-1 py-2 px-4 rounded', isLogin ? 'bg-blue-500 text-white' : 'bg-gray-200']"
        >
          Login
        </button>
        <button 
          @click="isLogin = false"
          :class="['flex-1 py-2 px-4 rounded', !isLogin ? 'bg-blue-500 text-white' : 'bg-gray-200']"
        >
          Sign Up
        </button>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="mb-4">
          <input
            v-model="email"
            type="email"
            placeholder="Email"
            class="w-full p-2 border rounded"
            required
          />
        </div>
        <div class="mb-4">
          <input
            v-model="password"
            type="password"
            placeholder="Password"
            class="w-full p-2 border rounded"
            required
          />
        </div>
        <button 
          type="submit"
          class="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
        >
          {{ isLogin ? 'Login' : 'Sign Up' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

const isLogin = ref(true)
const email = ref('')
const password = ref('')

const emit = defineEmits(['close'])

async function handleSubmit() {
  if (isLogin.value) {
    const success = await authStore.login({
      email: email.value,
      password: password.value
    })
    if (success) {
      emit('close')
      router.push('/profile')
    }
  } else {
    // Handle signup
  }
}
</script>