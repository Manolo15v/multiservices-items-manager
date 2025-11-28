import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { setAuthToken, clearAuthToken } from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = ref(false)

  const getUser = computed(() => user.value)
  const isLoggedIn = computed(() => isAuthenticated.value)
  
  /**
   * @param {string} token
   * @param {Object} userData
   */
  function login(token, userData) {
    setAuthToken(token)
    
    user.value = {
      id: userData.id,
      username: userData.username,
      email: userData.email,
    }
    
    isAuthenticated.value = true
  }

  function logout() {
    clearAuthToken()
    
    user.value = null
    isAuthenticated.value = false
  }

  /**
   * @param {Object} userData
   */
  function updateUser(userData) {
    if (user.value) {
      user.value = {
        ...user.value,
        ...userData
      }
    }
  }

  return {
    user,
    isAuthenticated,
    getUser,
    isLoggedIn,
    login,
    logout,
    updateUser
  }
})

