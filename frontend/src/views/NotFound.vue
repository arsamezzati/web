// views/NotFound.vue
<template>
  <div class="not-found">
    <i class="fas fa-exclamation-triangle"></i>
    <h1>404 - Page Not Found</h1>
    <p>The page you're looking for doesn't exist.</p>
    <router-link to="/" class="home-button">
      <i class="fas fa-home"></i> Go Home
    </router-link>
  </div>
</template>

<style scoped>
.not-found {
  text-align: center;
  padding: 4rem 2rem;
}

.not-found i {
  font-size: 4rem;
  color: #e74c3c;
  margin-bottom: 1rem;
}

.not-found h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 1rem;
}

.not-found p {
  color: #666;
  margin-bottom: 2rem;
}

.home-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  transition: background 0.2s;
}

.home-button:hover {
  background: #2563eb;
}
</style>