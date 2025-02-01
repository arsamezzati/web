import { createRouter, createWebHistory } from 'vue-router'

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
    path: '/about',  
    name: 'About',
    component: About
  },
  
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound  
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