<template>
  <Layout>
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold text-slate-800 mb-8">Dashboard</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <div class="bg-white rounded-xl shadow-md p-6 flex items-center space-x-4 hover:shadow-lg transition-shadow">
          <div class="w-16 h-16 bg-info-bg rounded-xl flex items-center justify-center text-3xl">
            📦
          </div>
          <div class="flex-1">
            <p class="text-sm text-slate-600 mb-1">Total Productos</p>
            <p class="text-3xl font-bold text-slate-800">{{ stats.totalProducts }}</p>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-md p-6 flex items-center space-x-4 hover:shadow-lg transition-shadow">
          <div class="w-16 h-16 bg-info-bg rounded-xl flex items-center justify-center text-3xl">
            📊
          </div>
          <div class="flex-1">
            <p class="text-sm text-slate-600 mb-1">Stock Total</p>
            <p class="text-3xl font-bold text-slate-800">{{ stats.totalStock }}</p>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-md p-6 flex items-center space-x-4 hover:shadow-lg transition-shadow">
          <div class="w-16 h-16 bg-warning-bg rounded-xl flex items-center justify-center text-3xl">
            ⚠️
          </div>
          <div class="flex-1">
            <p class="text-sm text-slate-600 mb-1">Stock Bajo</p>
            <p class="text-3xl font-bold text-slate-800">{{ stats.lowStock }}</p>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-md p-6 flex items-center space-x-4 hover:shadow-lg transition-shadow">
          <div class="w-16 h-16 bg-success-bg rounded-xl flex items-center justify-center text-3xl">
            💰
          </div>
          <div class="flex-1">
            <p class="text-sm text-slate-600 mb-1">Valor Total</p>
            <p class="text-3xl font-bold text-slate-800">${{ stats.totalValue }}</p>
          </div>
        </div>
      </div>

      <div class="mt-12">
        <h2 class="text-2xl font-semibold text-slate-800 mb-6">Acciones Rápidas</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <router-link 
            to="/products" 
            class="bg-white rounded-xl shadow-md p-6 flex flex-col items-center space-y-3 hover:shadow-lg hover:-translate-y-1 transition-all"
          >
            <span class="text-4xl">➕</span>
            <span class="text-base font-medium text-slate-700">Agregar Producto</span>
          </router-link>
          
          <router-link 
            to="/inventory" 
            class="bg-white rounded-xl shadow-md p-6 flex flex-col items-center space-y-3 hover:shadow-lg hover:-translate-y-1 transition-all"
          >
            <span class="text-4xl">📈</span>
            <span class="text-base font-medium text-slate-700">Gestionar Inventario</span>
          </router-link>
          
          <router-link 
            to="/products" 
            class="bg-white rounded-xl shadow-md p-6 flex flex-col items-center space-y-3 hover:shadow-lg hover:-translate-y-1 transition-all"
          >
            <span class="text-4xl">📋</span>
            <span class="text-base font-medium text-slate-700">Ver Productos</span>
          </router-link>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Layout from '../components/Layout.vue'
import { productsService } from '../services/productsService'
import { inventoryService } from '../services/inventoryService'

const stats = ref({
  totalProducts: 0,
  totalStock: 0,
  lowStock: 0,
  totalValue: 0
})

const loadStats = async () => {
  try {
    const [products, inventory] = await Promise.all([
      productsService.getAll().catch(() => ({ data: [] })),
      inventoryService.getAll().catch(() => ({ data: [] }))
    ])

    const productsData = products.data || products || []
    const inventoryData = inventory.data || inventory || []

    stats.value.totalProducts = productsData.length
    stats.value.totalStock = inventoryData.reduce((sum, item) => sum + (item.quantity || 0), 0)
    stats.value.lowStock = inventoryData.filter(item => (item.quantity || 0) < 10).length
    stats.value.totalValue = productsData.reduce((sum, p) => sum + (p.price || 0) * (inventoryData.find(i => i.product_id === p.id)?.quantity || 0), 0)
  } catch (error) {
    console.error('Error cargando estadísticas:', error)
  }
}

onMounted(() => {
  loadStats()
})
</script>
