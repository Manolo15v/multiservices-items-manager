import axios from 'axios'

const REQUEST_TIMEOUT = 10000

const AUTH_SERVICE_URL = import.meta.env.VITE_AUTH_SERVICE_URL
const PRODUCTS_SERVICE_URL = import.meta.env.VITE_PRODUCTS_SERVICE_URL
const INVENTORY_SERVICE_URL = import.meta.env.VITE_INVENTORY_SERVICE_URL

if (!AUTH_SERVICE_URL || !PRODUCTS_SERVICE_URL || !INVENTORY_SERVICE_URL) {
  console.error('Error: Las variables de entorno de los microservicios no están configuradas')
}

export const authApi = axios.create({
  baseURL: AUTH_SERVICE_URL,
  timeout: REQUEST_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true
})

export const productsApi = axios.create({
  baseURL: PRODUCTS_SERVICE_URL,
  timeout: REQUEST_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true
})

export const inventoryApi = axios.create({
  baseURL: INVENTORY_SERVICE_URL,
  timeout: REQUEST_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true
})

let authToken = null

/**
 * @param {string} token
 */
export function setAuthToken(token) {
  authToken = token
}

/**
 * @returns {string|null}
*/
export function getAuthToken() {
  return authToken
}

export function clearAuthToken() {
  authToken = null
}

const addAuthInterceptor = (apiInstance) => {
  apiInstance.interceptors.request.use(
    (config) => {
      const token = getAuthToken()
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  apiInstance.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        clearAuthToken()
        if (!window.location.pathname.includes('/login') && 
            !window.location.pathname.includes('/register')) {
          window.location.href = '/login'
        }
      }
      return Promise.reject(error)
    }
  )
}

addAuthInterceptor(authApi)
addAuthInterceptor(productsApi)
addAuthInterceptor(inventoryApi)

