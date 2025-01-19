<template>
    <div class="profile-container">
      <div v-if="authStore.isAuthenticated" class="profile-content">
        <div class="profile-header">
          <div class="profile-info">
            <div class="avatar">
              <i class="fas fa-user"></i>
            </div>
            <div class="user-details">
              <h1>{{ authStore.user.name }} {{ authStore.user.surname }}</h1>
              <p class="email">{{ authStore.user.email }}</p>
              <p class="member-since">Member since {{ formatDate(authStore.user.birthdate) }}</p>
            </div>
          </div>
        </div>
  
        <div class="stats-section">
          <div class="stat-card">
            <i class="fas fa-heart"></i>
            <div class="stat-info">
              <span class="stat-value">{{ likedGames.length }}</span>
              <span class="stat-label">Liked Games</span>
            </div>
          </div>
        </div>
  
        <div class="liked-games-section">
          <h2>Your Liked Games</h2>
          
          <div v-if="loading" class="loading">
            <i class="fas fa-spinner fa-spin"></i>
            Loading...
          </div>
  
          <div v-else-if="error" class="error">
            {{ error }}
          </div>
  
          <div v-else-if="likedGames.length === 0" class="no-games">
            <i class="fas fa-heart-broken"></i>
            <p>You haven't liked any games yet.</p>
            <router-link to="/games" class="browse-games-btn">
              Browse Games
            </router-link>
          </div>
  
          <div v-else class="games-grid">
            <div v-for="game in likedGames" :key="game.id" class="game-card">
              <div class="game-image">
                <img 
                  :src="game.cover?.url?.replace('t_thumb', 't_cover_big') || '/placeholder-game.jpg'" 
                  :alt="game.name"
                >
              </div>
              <div class="game-info">
                <h3>{{ game.name }}</h3>
                <div class="game-rating" v-if="game.rating">
                  <i class="fas fa-star"></i>
                  {{ Math.round(game.rating) / 10 }}/10
                </div>
                <p class="game-release" v-if="game.first_release_date">
                  Released: {{ formatGameDate(game.first_release_date) }}
                </p>
                <button 
                  class="unlike-button"
                  @click="toggleLike(game)"
                >
                  <i class="fas fa-heart"></i> Unlike
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <div v-else class="unauthorized">
        <i class="fas fa-lock"></i>
        <p>Please log in to view your profile.</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useAuthStore } from '../stores/authStore'
  
  const authStore = useAuthStore()
  const likedGames = ref([])
  const loading = ref(true)
  const error = ref(null)
  
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
  }
  
  const formatGameDate = (timestamp) => {
    const date = new Date(timestamp * 1000)
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long'
    })
  }
  
  const fetchLikedGames = async () => {
    if (!authStore.isAuthenticated) return
  
    try {
      loading.value = true
      error.value = null
      const response = await fetch(`http://localhost:5050/api/games/liked?user_id=${authStore.user.uid}`)
      if (!response.ok) throw new Error('Failed to fetch liked games')
      likedGames.value = await response.json()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }
  
  const toggleLike = async (game) => {
    try {
      const response = await fetch(
        `http://localhost:5050/api/games/${game.id}/like?user_id=${authStore.user.uid}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(game)
        }
      )
      
      if (!response.ok) throw new Error('Failed to unlike game')
      await fetchLikedGames() // Refresh the list
    } catch (e) {
      console.error('Error unliking game:', e)
    }
  }
  
  onMounted(() => {
    if (authStore.isAuthenticated) {
      fetchLikedGames()
    }
  })
  </script>
  
  <style scoped>
  .profile-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }
  
  .profile-header {
    background: white;
    border-radius: 8px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .profile-info {
    display: flex;
    align-items: center;
    gap: 2rem;
  }
  
  .avatar {
    width: 100px;
    height: 100px;
    background: #f8fafc;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    color: #3b82f6;
  }
  
  .user-details h1 {
    font-size: 2rem;
    color: #333;
    margin-bottom: 0.5rem;
  }
  
  .email {
    color: #666;
    margin-bottom: 0.5rem;
  }
  
  .member-since {
    color: #888;
    font-size: 0.875rem;
  }
  
  .stats-section {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .stat-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    flex: 1;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .stat-card i {
    font-size: 2rem;
    color: #3b82f6;
  }
  
  .stat-info {
    display: flex;
    flex-direction: column;
  }
  
  .stat-value {
    font-size: 1.5rem;
    font-weight: bold;
    color: #333;
  }
  
  .stat-label {
    color: #666;
    font-size: 0.875rem;
  }
  
  .liked-games-section {
    background: white;
    border-radius: 8px;
    padding: 2rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .liked-games-section h2 {
    font-size: 1.5rem;
    color: #333;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #3b82f6;
    display: inline-block;
  }
  
  .games-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
  }
  
  .game-card {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    border: 1px solid #eee;
  }
  
  .game-card:hover {
    transform: translateY(-5px);
  }
  
  .game-image {
    height: 200px;
    overflow: hidden;
  }
  
  .game-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .game-info {
    padding: 1.5rem;
  }
  
  .game-info h3 {
    margin: 0 0 0.5rem;
    font-size: 1.25rem;
    color: #333;
  }
  
  .game-rating {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: #f8fafc;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    color: #666;
    margin-bottom: 0.5rem;
  }
  
  .game-rating i {
    color: #f59e0b;
  }
  
  .game-release {
    color: #666;
    font-size: 0.875rem;
    margin-bottom: 1rem;
  }
  
  .unlike-button {
    width: 100%;
    padding: 0.75rem;
    background: #ef4444;
    color: white;
    border: none;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    cursor: pointer;
    transition: background 0.2s;
  }
  
  .unlike-button:hover {
    background: #dc2626;
  }
  
  .loading {
    text-align: center;
    padding: 2rem;
    color: #666;
  }
  
  .loading i {
    margin-right: 0.5rem;
  }
  
  .error {
    text-align: center;
    padding: 2rem;
    color: #dc2626;
    background: #fee2e2;
    border-radius: 8px;
  }
  
  .no-games {
    text-align: center;
    padding: 3rem;
    color: #666;
  }
  
  .no-games i {
    font-size: 3rem;
    color: #9ca3af;
    margin-bottom: 1rem;
  }
  
  .browse-games-btn {
    display: inline-block;
    margin-top: 1rem;
    padding: 0.75rem 1.5rem;
    background: #3b82f6;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    transition: background 0.2s;
  }
  
  .browse-games-btn:hover {
    background: #2563eb;
  }
  
  .unauthorized {
    text-align: center;
    padding: 4rem 2rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .unauthorized i {
    font-size: 3rem;
    color: #9ca3af;
    margin-bottom: 1rem;
  }
  
  .unauthorized p {
    color: #666;
    font-size: 1.25rem;
  }
  
  @media (max-width: 768px) {
    .profile-info {
      flex-direction: column;
      text-align: center;
    }
  
    .stats-section {
      flex-direction: column;
    }
  
    .games-grid {
      grid-template-columns: 1fr;
    }
  }
  </style>