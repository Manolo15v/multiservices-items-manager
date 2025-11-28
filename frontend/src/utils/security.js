

/**
 * @param {string} input
 * @returns {string}
 */
export function sanitizeInput(input) {
  if (typeof input !== 'string') return input
  
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
    '/': '&#x2F;',
  }
  
  return input.replace(/[&<>"'/]/g, (char) => map[char])
}

/**
 * @param {string} email
 * @returns {boolean}
 */
export function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * @param {string} password
 * @returns {Object}
 */
export function validatePassword(password) {
  if (password.length < 8) {
    return {
      isValid: false,
      message: 'La contraseña debe tener al menos 8 caracteres'
    }
  }
  
  if (!/[a-z]/.test(password)) {
    return {
      isValid: false,
      message: 'La contraseña debe contener al menos una letra minúscula'
    }
  }
  
  if (!/[A-Z]/.test(password)) {
    return {
      isValid: false,
      message: 'La contraseña debe contener al menos una letra mayúscula'
    }
  }
  
  if (!/[0-9]/.test(password)) {
    return {
      isValid: false,
      message: 'La contraseña debe contener al menos un número'
    }
  }
  
  return {
    isValid: true,
    message: 'Contraseña válida'
  }
}

/**
 * @param {Object} obj
 * @returns {Object}
 */
export function sanitizePayload(obj) {
  const sensitiveKeys = ['password', 'token', 'secret', 'apiKey', 'privateKey']
  const cleaned = { ...obj }
  
  Object.keys(cleaned).forEach(key => {
    if (sensitiveKeys.some(sensitive => key.toLowerCase().includes(sensitive.toLowerCase()))) {
      Object.defineProperty(cleaned, key, {
        enumerable: true,
        value: cleaned[key]
      })
    }
  })
  
  return cleaned
}

