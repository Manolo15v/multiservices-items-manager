<template>
  <div class="min-h-screen flex flex-col bg-slate-50">
    <nav class="bg-white shadow-sm border-b border-slate-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex-shrink-0">
            <h2 class="text-xl font-bold text-primary-dark">Microservicios Manager</h2>
          </div>
          
          <div class="hidden md:flex items-center space-x-4">
            <router-link 
              to="/dashboard" 
              class="px-4 py-2 rounded-md text-sm font-medium text-slate-700 hover:bg-slate-100 hover:text-slate-900 transition-colors"
              active-class="bg-primary text-white hover:bg-primary-dark hover:text-white"
            >
              Dashboard
            </router-link>
            <router-link 
              to="/products" 
              class="px-4 py-2 rounded-md text-sm font-medium text-slate-700 hover:bg-slate-100 hover:text-slate-900 transition-colors"
              active-class="bg-primary text-white hover:bg-primary-dark hover:text-white"
            >
              Productos
            </router-link>
            <router-link 
              to="/inventory" 
              class="px-4 py-2 rounded-md text-sm font-medium text-slate-700 hover:bg-slate-100 hover:text-slate-900 transition-colors"
              active-class="bg-primary text-white hover:bg-primary-dark hover:text-white"
            >
              Inventario
            </router-link>
          </div>

          <div class="flex items-center space-x-4">
            <span class="text-sm font-medium text-slate-600 hidden sm:block">
              {{ authStore.getUser?.username }}
            </span>
            <button 
              @click="handleLogout" 
              class="px-4 py-2 bg-danger hover:bg-danger-light text-white text-sm font-medium rounded-md transition-colors"
            >
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="flex-1 p-4 md:p-8">
      <slot></slot>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
