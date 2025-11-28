import { inventoryApi } from './api'

export const inventoryService = {
  /**
   * @returns {Promise}
   */
  async getAll() {
    try {
      const response = await inventoryApi.get('/inventory')
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  /**
   * @param {number|string} productId
   * @returns {Promise}
   */
  async getByProductId(productId) {
    try {
      const response = await inventoryApi.get(`/inventory/${productId}`)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  /**
   * @param {number|string} productId
   * @param {number} quantity
   * @returns {Promise}
   */
  async increaseStock(productId, quantity) {
    try {
      const response = await inventoryApi.post(`/inventory/${productId}/increase`, { quantity })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  /**
   * @param {number|string} productId
   * @param {number} quantity
   * @returns {Promise}
   */
  async decreaseStock(productId, quantity) {
    try {
      const response = await inventoryApi.post(`/inventory/${productId}/decrease`, { quantity })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  /**
   * @param {number|string} productId
   * @param {number} quantity
   * @returns {Promise}
   */
  async setStock(productId, quantity) {
    try {
      const response = await inventoryApi.put(`/inventory/${productId}`, { quantity })
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  }
}

