import { authApi } from './api'

export const authService = {
  /**
   * @param {Object} userData
   * @returns {Promise}
   */
  async register(userData) {
    try {
      const response = await authApi.post('/register', userData)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  /**
   * @param {Object} credentials
   * @returns {Promise}
   */
  async login(credentials) {
    try {
      const response = await authApi.post('/login', credentials)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  /**
   * @returns {Promise}
   */
  async validateToken() {
    try {
      const response = await authApi.get('/validate')
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

}

