<template>
  <nav class="navbar">
    <div class="container">
      <router-link to="/" class="logo">
        <i class="fas fa-gamepad"></i>
        GameTracker
      </router-link>

      <div class="nav-links">
        <router-link to="/games" class="nav-link">
          <i class="fas fa-gamepad"></i>
          <span>Games</span>
        </router-link>
        <template v-if="authStore.isAuthenticated">
          <div class="profile-dropdown" @mouseleave="closeDropdown" @mouseenter="openDropdown">
            <button class="nav-link login-button">
              <i class="fas fa-user"></i>
              <span>Profile</span>
            </button>
            <div class="dropdown-content" :class="{ 'show': isDropdownOpen }">
              <router-link to="/profile" class="dropdown-item">
                <i class="fas fa-user-circle"></i>
                {{ authStore.user.name }}'s Profile
              </router-link>
              <button @click="handleLogout" class="dropdown-item">
                <i class="fas fa-sign-out-alt"></i>
                Logout
              </button>
            </div>
          </div>
        </template>
        <template v-else>
          <button @click="toggleLoginModal" class="nav-link login-button">
            <i class="fas fa-user"></i>
            <span>Login/Signup</span>
          </button>
        </template>
        <button @click="testAuth" class="nav-link login-button">Test Auth</button>
      </div>
    </div>
    <LoginModal v-model:show="isLoginModalOpen" />
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import LoginModal from './Login.vue'
import { useAuthStore } from '../stores/AuthStore'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoginModalOpen = ref(false)
const authStore = useAuthStore()
const isDropdownOpen = ref(false)

const testAuth = () => {
  console.log("Auth State:", authStore.isAuthenticated, authStore.user)
}

const toggleLoginModal = () => {
  isLoginModalOpen.value = true
}

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

const openDropdown = () => {
  isDropdownOpen.value = true
}

const closeDropdown = () => {
  isDropdownOpen.value = false
}
</script>

<style scoped>
.navbar {
 background: #1a1a1a;
 color: white;
 position: sticky;
 top: 0;
 z-index: 50;
 box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.container {
 max-width: 1200px;
 margin: 0 auto;
 padding: 0 1rem;
 display: flex;
 justify-content: space-between;
 align-items: center;
 height: 4rem;
}

.logo {
 font-size: 1.5rem;
 font-weight: bold;
 color: white;
 text-decoration: none;
 display: flex;
 align-items: center;
 gap: 0.5rem;
 transition: color 0.2s;
 height: 4rem;
}

.logo i {
 color: #3b82f6;
}

.logo:hover {
 color: #3b82f6;
}

.nav-links {
 display: flex;
 gap: 2rem;
 align-items: center;
 height: 100%;
}

.nav-link {
 height: 4rem;
 color: white;
 text-decoration: none;
 display: flex;
 align-items: center;
 gap: 0.5rem;
 padding: 0 0.5rem;
 border-bottom: 2px solid transparent;
 transition: all 0.2s;
}

.nav-link:hover {
 color: #3b82f6;
 border-bottom-color: #3b82f6;
}

.nav-link.router-link-active {
 border-bottom-color: #3b82f6;
}

.login-button {
 height: 4rem;
 background: none;
 border: none;
 color: white;
 font-size: inherit;
 font-family: inherit;
 cursor: pointer;
 padding: 0 0.5rem;
 display: flex;
 align-items: center;
 gap: 0.5rem;
}

.profile-dropdown {
 position: relative;
 height: 4rem;
}

.profile-dropdown .nav-link,
.profile-dropdown .login-button {
 height: 4rem;
 padding: 0 0.5rem;
}

.dropdown-content {
 visibility: hidden;
 opacity: 0;
 position: absolute;
 right: 0;
 top: 100%;
 background: #1a1a1a;
 min-width: 180px;
 box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
 border-radius: 4px;
 z-index: 100;
 transform: translateY(-10px);
 transition: all 0.3s ease;
}

.dropdown-content.show {
 visibility: visible;
 opacity: 1;
 transform: translateY(0);
}

.dropdown-item {
 display: flex;
 align-items: center;
 gap: 0.75rem;
 padding: 0.75rem 1rem;
 color: white;
 text-decoration: none;
 transition: all 0.2s ease;
 border: none;
 width: 100%;
 text-align: left;
 font-size: inherit;
 font-family: inherit;
 background: none;
 cursor: pointer;
 white-space: nowrap;
}

.dropdown-item:first-child {
 border-radius: 4px 4px 0 0;
}

.dropdown-item:last-child {
 border-radius: 0 0 4px 4px;
}

.dropdown-item:hover {
 background: #2d2d2d;
 color: #3b82f6;
}

.dropdown-item i {
 width: 1rem;
}

.dropdown-content::before {
 content: '';
 position: absolute;
 top: -4px;
 right: 20px;
 width: 8px;
 height: 8px;
 background: #1a1a1a;
 transform: rotate(45deg);
}

/* Media Queries for Responsiveness */
@media (max-width: 768px) {
 .nav-links {
   gap: 1rem;
 }
 
 .nav-link span {
   display: none;
 }
 
 .dropdown-content {
   right: -2rem;
 }
 
 .dropdown-content::before {
   right: 2.5rem;
 }
}

@media (max-width: 480px) {
 .container {
   padding: 0 0.5rem;
 }
 
 .logo span {
   display: none;
 }
}
</style>