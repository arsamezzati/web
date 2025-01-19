<template>
    <div class="games-container">
      <div class="search-section">
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search games..."
            @input="handleSearch"
          >
        </div>
      </div>
  
      <div v-if="loading" class="loading">
        <i class="fas fa-spinner fa-spin"></i>
        Loading...
      </div>
  
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
  
      <div v-else class="games-grid">
        <div v-for="game in games" :key="game.id" class="game-card">
          <div class="game-image">
            <img 
              :src="game.cover?.url?.replace('t_thumb', 't_cover_big') || '/placeholder-game.jpg'" 
              :alt="game.name"
            >
          </div>
          <div class="game-info">
            <div class="game-header">
              <h3>{{ game.name }}</h3>
              <button 
                v-if="authStore.isAuthenticated"
                class="like-button" 
                :class="{ liked: likedGames.has(game.id) }"
                @click="toggleLike(game)"
              >
                <i class="fas" :class="likedGames.has(game.id) ? 'fa-heart' : 'fa-heart'"></i>
              </button>
            </div>
            <div class="game-rating" v-if="game.rating">
              <i class="fas fa-star"></i>
              {{ Math.round(game.rating) / 10 }}/10
            </div>
            <p class="game-release" v-if="game.first_release_date">
              Released: {{ new Date(game.first_release_date * 1000).getFullYear() }}
            </p>
            <p class="game-summary">{{ truncateSummary(game.summary) }}</p>
            <div class="comments-section" v-if="selectedGame === game.id">
  <div class="comments-container">
    <h4 class="comments-title">Comments</h4>
    
    <!-- Comment Form -->
    <form v-if="authStore.isAuthenticated" @submit.prevent="submitComment(game.id)" class="comment-form">
      <textarea 
        v-model="newComment"
        placeholder="Write a comment..."
        class="comment-input"
        rows="3"
      ></textarea>
      <button type="submit" class="comment-submit">
        <i class="fas fa-paper-plane"></i> Post Comment
      </button>
    </form>
    <div v-else class="login-prompt">
      Please <a href="#" @click.prevent="$emit('login')">login</a> to comment
    </div>

    <!-- Comments List -->
    <div class="comments-list">
      <div v-for="comment in gameComments[game.id] || []" :key="comment._id" class="comment">
        <div class="comment-header">
          <span class="comment-author">{{ comment.user_name }}</span>
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>
        <p class="comment-content">{{ comment.content }}</p>
      </div>
      <div v-if="!gameComments[game.id]?.length" class="no-comments">
        No comments yet. Be the first to comment!
      </div>
    </div>
  </div>
</div>

<!-- Add a comment toggle button -->
<button @click="toggleComments(game.id)" class="comment-toggle">
  <i class="fas fa-comments"></i>
  Comments
</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { debounce } from 'lodash'
  import { useAuthStore } from '../stores/authStore'
  
  const authStore = useAuthStore()
  const games = ref([])
  const loading = ref(true)
  const error = ref(null)
  const searchQuery = ref('')
  const likedGames = ref(new Set())
  
  const fetchPopularGames = async () => {
    try {
      loading.value = true
      error.value = null
      const response = await fetch('http://localhost:5050/api/games/popular')
      if (!response.ok) throw new Error('Failed to fetch games')
      games.value = await response.json()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  const fetchLikedGames = async () => {
    if (!authStore.isAuthenticated) return
    
    try {
      const response = await fetch(`http://localhost:5050/api/games/liked?user_id=${authStore.user.uid}`)
      if (!response.ok) throw new Error('Failed to fetch liked games')
      const likedGamesData = await response.json()
      likedGames.value = new Set(likedGamesData.map(game => game.id))
    } catch (e) {
      console.error('Error fetching liked games:', e)
    }
  }

  const toggleLike = async (game) => {
    if (!authStore.isAuthenticated) {
      // You might want to trigger login modal here
      return
    }

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

      if (!response.ok) throw new Error('Failed to toggle like')
      
      const { liked } = await response.json()
      if (liked) {
        likedGames.value.add(game.id)
      } else {
        likedGames.value.delete(game.id)
      }
    } catch (e) {
      console.error('Error toggling like:', e)
    }
  }
  
  const handleSearch = debounce(async () => {
    if (!searchQuery.value.trim()) {
      await fetchPopularGames()
      return
    }
  
    try {
      loading.value = true
      error.value = null
      const response = await fetch(`http://localhost:5050/api/games/search?query=${encodeURIComponent(searchQuery.value)}`)
      if (!response.ok) throw new Error('Failed to search games')
      games.value = await response.json()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }, 300)
  
  const truncateSummary = (summary) => {
    if (!summary) return 'No summary available'
    return summary.length > 100 ? summary.slice(0, 100) + '...' : summary
  }
  
  onMounted(async () => {
    await fetchPopularGames()
    if (authStore.isAuthenticated) {
      await fetchLikedGames()
    }
  })
  const selectedGame = ref(null)
const newComment = ref('')
const gameComments = ref({})

const toggleComments = async (gameId) => {
  if (selectedGame.value === gameId) {
    selectedGame.value = null
  } else {
    selectedGame.value = gameId
    await fetchComments(gameId)
  }
}

const fetchComments = async (gameId) => {
  try {
    const response = await fetch(`http://localhost:5050/api/games/${gameId}/comments`)
    if (!response.ok) throw new Error('Failed to fetch comments')
    const comments = await response.json()
    gameComments.value[gameId] = comments
  } catch (e) {
    console.error('Error fetching comments:', e)
  }
}

const submitComment = async (gameId) => {
  if (!newComment.value.trim()) return

  try {
    const response = await fetch(`http://localhost:5050/api/games/${gameId}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: newComment.value.trim(),
        game_id: gameId,
        user_id: authStore.user.uid,
        user_name: `${authStore.user.name} ${authStore.user.surname}`
      })
    })

    if (!response.ok) throw new Error('Failed to post comment')
    
    // Clear the input and refresh comments
    newComment.value = ''
    await fetchComments(gameId)
  } catch (e) {
    console.error('Error posting comment:', e)
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
  </script>
  
  <style scoped>
  .games-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }
  
  .search-section {
    margin-bottom: 2rem;
  }
  
  .search-box {
    position: relative;
    max-width: 600px;
    margin: 0 auto;
  }
  
  .search-box i {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: #666;
  }
  
  .search-box input {
    width: 100%;
    padding: 1rem 1rem 1rem 3rem;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.2s;
  }
  
  .search-box input:focus {
    border-color: #3b82f6;
    outline: none;
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

  .game-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.5rem;
  }
  
  .game-info h3 {
    margin: 0;
    font-size: 1.25rem;
    color: #333;
    flex: 1;
    padding-right: 1rem;
  }

  .like-button {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1.25rem;
    color: #666;
    padding: 0.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
  }

  .like-button:hover {
    background: #f8fafc;
    transform: scale(1.1);
  }

  .like-button.liked {
    color: #ef4444;
  }

  .like-button.liked:hover {
    color: #dc2626;
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
    margin-bottom: 0.5rem;
  }
  
  .game-summary {
    color: #666;
    font-size: 0.875rem;
    line-height: 1.5;
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
  }
  
  @media (max-width: 768px) {
    .games-container {
      padding: 1rem;
    }
    
    .games-grid {
      grid-template-columns: 1fr;
    }
  }
  .comments-section {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.comments-title {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 1rem;
}

.comment-form {
  margin-bottom: 1.5rem;
}

.comment-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  margin-bottom: 0.5rem;
}

.comment-submit {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.comment-submit:hover {
  background: #2563eb;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comment {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 4px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-weight: 600;
  color: #333;
}

.comment-date {
  color: #666;
  font-size: 0.875rem;
}

.comment-content {
  color: #444;
  line-height: 1.5;
}

.login-prompt {
  text-align: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.login-prompt a {
  color: #3b82f6;
  text-decoration: none;
}

.no-comments {
  text-align: center;
  color: #666;
  padding: 1rem;
}

.comment-toggle {
  margin-top: 1rem;
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  font-size: 0.875rem;
}

.comment-toggle:hover {
  color: #3b82f6;
}
  </style>