// stores/plugins/piniaPluginPersistedstate.js
import { createPersistedState } from 'pinia-plugin-persistedstate'

export const piniaPluginPersistedstate = createPersistedState({
  storage: localStorage,
  key: prefix => `gametracker-${prefix}`
})