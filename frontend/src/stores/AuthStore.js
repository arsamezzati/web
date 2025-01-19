
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        isAuthenticated: false,
        user: null,
        loading: false
    }),
    getters: {
        //getter
        isLoggedIn: (state) => state.isAuthenticated && state.user !== null
    },
    actions: {
        setUser(userData) {
            console.log('Setting user in store:', userData)
            this.user = userData
            this.isAuthenticated = true
        },
        logout() {
            console.log('Logging out user from store')
            this.user = null
            this.isAuthenticated = false
        }
    },
    persist: {
        key: 'auth',
        storage: localStorage,
        paths: ['user', 'isAuthenticated']  
    }
})