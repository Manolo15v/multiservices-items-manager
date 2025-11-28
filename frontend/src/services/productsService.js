import { productsApi } from './api'

export const productsService = {
  /**
   * @returns {Promise}
   */
  async getAll() {
    try {
      const response = await productsApi.get('/products')
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  /**
   * @param {number|string} id
   * @returns {Promise}
   */
  async getById(id) {
    try {
      const response = await productsApi.get(`/products/${id}`)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  /**
   * @param {Object} productData
   * @returns {Promise}
   */
  async create(productData) {
    try {
      const response = await productsApi.post('/products', productData)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  /**
   * @param {number|string} id
   * @param {Object} productData
   * @returns {Promise}
   */
  async update(id, productData) {
    try {
      const response = await productsApi.put(`/products/${id}`, productData)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  },

  /**
   * @param {number|string} id
   * @returns {Promise}
   */
  async delete(id) {
    try {
      const response = await productsApi.delete(`/products/${id}`)
      return response.data
    } catch (error) {
      throw error.response?.data || error.message
    }
  }
}

