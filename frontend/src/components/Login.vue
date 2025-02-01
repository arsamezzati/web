<template>
    <Transition name="modal">
      <div v-if="show" class="modal-overlay" @click.self="closeModal">
        <div class="modal-container">
          <div class="modal-header">
            <div class="tab-container">
              <button 
                :class="['tab-button', { active: isLogin }]" 
                @click="isLogin = true"
              >
                Login
              </button>
              <button 
                :class="['tab-button', { active: !isLogin }]" 
                @click="isLogin = false"
              >
                Register
              </button>
            </div>
            <button class="close-button" @click="closeModal">&times;</button>
          </div>
  
          <div class="modal-content">
            <form @submit.prevent="handleSubmit">
              <div class="form-group">
                <label>Email</label>
                <input 
                  type="email" 
                  v-model="formData.email" 
                  required 
                  placeholder="Enter your email"
                >
              </div>
  
              <template v-if="!isLogin">
                <div class="form-group">
                  <label>Name</label>
                  <input 
                    type="text" 
                    v-model="formData.name" 
                    required 
                    placeholder="Enter your name"
                  >
                </div>
  
                <div class="form-group">
                  <label>Surname</label>
                  <input 
                    type="text" 
                    v-model="formData.surname" 
                    required 
                    placeholder="Enter your surname"
                  >
                </div>
  
                <div class="form-group">
                  <label>Birthdate</label>
                  <input 
                    type="date" 
                    v-model="formData.birthdate" 
                    required
                  >
                </div>
              </template>
  
              <div class="form-group">
                <label>Password</label>
                <input 
                  type="password" 
                  v-model="formData.password" 
                  required 
                  placeholder="Enter your password"
                >
              </div>
  
              <div class="form-group" v-if="!isLogin">
                <label>Confirm Password</label>
                <input 
                  type="password" 
                  v-model="formData.confirmPassword" 
                  required 
                  placeholder="Confirm your password"
                >
              </div>
  
              <button type="submit" class="submit-button" :disabled="loading">
                {{ loading ? 'Please wait...' : (isLogin ? 'Login' : 'Register') }}
              </button>
            </form>
  
            <div v-if="error" class="error-message">
              {{ error }}
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </template>
  
  <script setup>
  import { ref, reactive } from 'vue'
  import { useAuthStore } from '../stores/authStore'
  import { useRouter } from 'vue-router'
  
  const props = defineProps({
    show: {
      type: Boolean,
      required: true
    }
  })
  
  const emit = defineEmits(['update:show'])
  const router = useRouter()
  const authStore = useAuthStore()
  
  const isLogin = ref(true)
  const loading = ref(false)
  const error = ref('')
  
  const formData = reactive({
    email: '',
    name: '',
    surname: '',
    password: '',
    confirmPassword: '',
    birthdate: ''
  })
  
  const closeModal = () => {
    emit('update:show', false)
    resetForm()
  }
  
  const resetForm = () => {
    formData.email = ''
    formData.name = ''
    formData.surname = ''
    formData.password = ''
    formData.confirmPassword = ''
    formData.birthdate = ''
    error.value = ''
  }
  
  const handleSubmit = async () => {
  error.value = ''
  loading.value = true

  try {
    if (!isLogin.value && formData.password !== formData.confirmPassword) {
      throw new Error('Passwords do not match')
    }

    const endpoint = isLogin.value ? '/api/login' : '/api/register'
    
    
    const payload = isLogin.value ? {
      email: formData.email,
      password: formData.password
    } : {
      email: formData.email.trim(),
      password: formData.password,
      name: formData.name.trim(),
      surname: formData.surname.trim(),
      birthdate: formData.birthdate  
    }

    console.log('Sending payload:', payload)  

    const response = await fetch(`http://localhost:5050${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    })

    if (!response.ok) {
      const errorData = await response.json()
      console.error('Server response:', errorData)  
      throw new Error(errorData.detail || 'Authentication failed')
    }

    const userData = await response.json()
    console.log('Received user data:', userData) 
    authStore.setUser(userData)
    closeModal()
    router.push('/profile')

  } catch (e) {
    console.error('Error:', e) 
    error.value = e.message
  } finally {
    loading.value = false
  }
}
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-container {
    background: white;
    width: 90%;
    max-width: 400px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }
  
  .modal-header {
    padding: 1rem;
    border-bottom: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .tab-container {
    display: flex;
    gap: 1rem;
  }
  
  .tab-button {
    padding: 0.5rem 1rem;
    border: none;
    background: none;
    cursor: pointer;
    font-weight: 500;
    color: #666;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
  }
  
  .tab-button.active {
    color: #3b82f6;
    border-bottom-color: #3b82f6;
  }
  
  .close-button {
    border: none;
    background: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #666;
  }
  
  .modal-content {
    padding: 1.5rem;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: #333;
    font-weight: 500;
  }
  
  .form-group input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  .submit-button {
    width: 100%;
    padding: 0.75rem;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.2s;
  }
  
  .submit-button:hover {
    background: #2563eb;
  }
  
  .submit-button:disabled {
    background: #93c5fd;
    cursor: not-allowed;
  }
  
  .error-message {
    margin-top: 1rem;
    padding: 0.75rem;
    background: #fee2e2;
    border: 1px solid #fecaca;
    border-radius: 4px;
    color: #dc2626;
  }
  
  .modal-enter-active,
  .modal-leave-active {
    transition: opacity 0.3s ease;
  }
  
  .modal-enter-from,
  .modal-leave-to {
    opacity: 0;
  }
  </style>