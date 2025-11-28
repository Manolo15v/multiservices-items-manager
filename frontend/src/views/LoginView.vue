<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary to-primary-dark p-4">
    <div class="bg-white rounded-xl shadow-xl p-12 w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-slate-800 mb-2">Iniciar Sesión</h1>
        <p class="text-slate-600 text-sm">Ingresa tus credenciales para acceder</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
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
            class="w-full px-4 py-3 border-2 border-slate-200 rounded-lg text-base transition-all outline-none focus:border-primary focus:ring-4 focus:ring-primary/10 disabled:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
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
            class="w-full px-4 py-3 border-2 border-slate-200 rounded-lg text-base transition-all outline-none focus:border-primary focus:ring-4 focus:ring-primary/10 disabled:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
          />
        </div>

        <div v-if="error" class="bg-danger-bg text-danger px-4 py-3 rounded-lg text-sm text-center">
          {{ error }}
        </div>

        <button 
          type="submit" 
          :disabled="loading"
          class="w-full bg-gradient-to-r from-primary to-primary-dark text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300 hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none"
        >
          <span v-if="!loading">Iniciar Sesión</span>
          <span v-else>Cargando...</span>
        </button>
      </form>

      <div class="mt-8 text-center text-sm text-slate-600">
        <p>
          ¿No tienes cuenta? 
          <router-link to="/register" class="text-primary font-semibold hover:underline">
            Regístrate
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { authService } from '../services/authService'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  email: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await authService.login({
      email: formData.value.email,
      password: formData.value.password
    })

    authStore.login(response.token, response.user)
    router.push('/dashboard')
  } catch (err) {
    error.value = err.message || 'Error al iniciar sesión. Verifica tus credenciales.'
  } finally {
    loading.value = false
  }
}
</script>
