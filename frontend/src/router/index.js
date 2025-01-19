// index.js (router configuration)
import { createRouter, createWebHistory } from 'vue-router'

// Import views
import Home from '../views/home.vue'
import About from '../views/About.vue'
import NotFound from '../views/NotFound.vue'
import Games from '../views/Games.vue'
import profile from '../views/Profile.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',  // Changed from '/' to '/about'
    name: 'About',
    component: About
  },
  // NotFound should always be last
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound  // Using direct import since we already imported it
  },
  {
    path: '/games',
    name: 'Games',
    component: Games

  },
  {
    path:'/profile',
    name: 'Profile',
    component: profile
  }
  
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  }
})

router.onError((error) => {
  if (error.message.includes('Failed to fetch dynamically imported module')) {
    router.push({ name: 'NotFound' })
  }
})

export default router