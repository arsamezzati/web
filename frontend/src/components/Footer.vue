// components/Footer.vue
<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-section">
          <h2>Why Choose Us</h2>
          <ul class="feature-list">
            <li><i class="fas fa-check"></i>Track your gaming progress</li>
            <li><i class="fas fa-check"></i>Connect with other gamers</li>
            <li><i class="fas fa-check"></i>Discover new games</li>
          </ul>
        </div>

        <!--  Links -->
        <div class="footer-section">
          <h2>Quick Links</h2>
          <ul class="link-list">
            <li>
              <router-link to="/about">
                <i class="fas fa-angle-right"></i>About Us
              </router-link>
            </li>
            <li>
              <router-link to="/contact">
                <i class="fas fa-angle-right"></i>Contact
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Social Links -->
        <div class="footer-section">
          <h2>Connect With Us</h2>
          <div class="social-links">
            <a href="#" title="Twitter"><i class="fab fa-twitter"></i></a>
            <a href="#" title="Discord"><i class="fab fa-discord"></i></a>
            <a href="#" title="GitHub"><i class="fab fa-github"></i></a>
          </div>
        </div>
      </div>
      
      <div class="copyright">
        <p>© 2024 GameTracker. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #1a1a1a;
  color: white;
  margin-top: auto;
  border-top: 1px solid #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3rem;
}

@media (max-width: 768px) {
  .footer-grid {
    grid-template-columns: 1fr;
  }
}

.footer-section h2 {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #3b82f6;
  display: inline-block;
}

.feature-list, .link-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.feature-list li, .link-list li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: transform 0.2s;
}

.feature-list li:hover, .link-list li:hover {
  transform: translateX(0.5rem);
}

.feature-list i {
  color: #3b82f6;
}

.link-list a {
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: color 0.2s;
}

.link-list a:hover {
  color: #3b82f6;
}

.social-links {
  display: flex;
  gap: 1.5rem;
}

.social-links a {
  color: white;
  font-size: 1.5rem;
  text-decoration: none;
  transition: all 0.2s;
}

.social-links a:hover {
  color: #3b82f6;
  transform: scale(1.1);
}

.copyright {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #333;
  text-align: center;
  color: #999;
}
</style>