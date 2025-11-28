<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-secondary to-secondary-dark p-4">
    <div class="bg-white rounded-xl shadow-xl p-12 w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-slate-800 mb-2">Crear Cuenta</h1>
        <p class="text-slate-600 text-sm">Completa el formulario para registrarte</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-6">
        <div class="space-y-2">
          <label for="username" class="block text-sm font-semibold text-slate-700">
            Nombre de usuario
          </label>
          <input
            id="username"
            v-model="formData.username"
            type="text"
            placeholder="usuario123"
            required
            :disabled="loading"
            class="w-full px-4 py-3 border-2 border-slate-200 rounded-lg text-base transition-all outline-none focus:border-secondary focus:ring-4 focus:ring-secondary/10 disabled:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
          />
        </div>

        <div class="space-y-2">
          <label for="email" class="block text-sm font-semibold text-slate-700">
            Email
          </label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            placeholder="tu@email.com"
            required
            :disabled="loading"
            class="w-full px-4 py-3 border-2 border-slate-200 rounded-lg text-base transition-all outline-none focus:border-secondary focus:ring-4 focus:ring-secondary/10 disabled:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
          />
        </div>

        <div class="space-y-2">
          <label for="password" class="block text-sm font-semibold text-slate-700">
            Contraseña
          </label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            placeholder="••••••••"
            required
            :disabled="loading"
            class="w-full px-4 py-3 border-2 border-slate-200 rounded-lg text-base transition-all outline-none focus:border-secondary focus:ring-4 focus:ring-secondary/10 disabled:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
          />
          <small 
            v-if="passwordStrength" 
            :class="[
              'text-xs block mt-1',
              passwordStrength.class === 'valid' ? 'text-success' : 'text-danger'
            ]"
          >
            {{ passwordStrength.message }}
          </small>
        </div>

        <div class="space-y-2">
          <label for="confirmPassword" class="block text-sm font-semibold text-slate-700">
            Confirmar contraseña
          </label>
          <input
            id="confirmPassword"
            v-model="formData.confirmPassword"
            type="password"
            placeholder="••••••••"
            required
            :disabled="loading"
            class="w-full px-4 py-3 border-2 border-slate-200 rounded-lg text-base transition-all outline-none focus:border-secondary focus:ring-4 focus:ring-secondary/10 disabled:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
          />
        </div>

        <div v-if="error" class="bg-danger-bg text-danger px-4 py-3 rounded-lg text-sm text-center">
          {{ error }}
        </div>

        <button 
          type="submit" 
          :disabled="loading || !isFormValid"
          class="w-full bg-gradient-to-r from-secondary to-secondary-dark text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300 hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none"
        >
          <span v-if="!loading">Registrarse</span>
          <span v-else>Registrando...</span>
        </button>
      </form>

      <div class="mt-8 text-center text-sm text-slate-600">
        <p>
          ¿Ya tienes cuenta? 
          <router-link to="/login" class="text-secondary font-semibold hover:underline">
            Inicia sesión
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { authService } from '../services/authService'
import { validatePassword, isValidEmail } from '../utils/security'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref('')

const passwordStrength = computed(() => {
  if (!formData.value.password) return null
  
  const validation = validatePassword(formData.value.password)
  return {
    message: validation.message,
    class: validation.isValid ? 'valid' : 'invalid'
  }
})

const isFormValid = computed(() => {
  return (
    formData.value.username &&
    isValidEmail(formData.value.email) &&
    validatePassword(formData.value.password).isValid &&
    formData.value.password === formData.value.confirmPassword
  )
})

const handleRegister = async () => {
  if (!isFormValid.value) {
    error.value = 'Por favor completa todos los campos correctamente'
    return
  }

  if (formData.value.password !== formData.value.confirmPassword) {
    error.value = 'Las contraseñas no coinciden'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const response = await authService.register({
      username: formData.value.username,
      email: formData.value.email,
      password: formData.value.password
    })

    authStore.login(response.token, response.user)
    router.push('/dashboard')
  } catch (err) {
    error.value = err.message || 'Error al registrarse. Por favor intenta de nuevo.'
  } finally {
    loading.value = false
  }
}
</script>
