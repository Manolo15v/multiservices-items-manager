<template>
  <Layout>
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold text-slate-800 mb-8">Gestión de Inventario</h1>

      <div v-if="loading" class="text-center py-12 text-slate-600">
        Cargando inventario...
      </div>
      
      <div v-else-if="error" class="bg-danger-bg text-danger px-4 py-3 rounded-lg text-center">
        {{ error }}
      </div>
      
      <div v-else-if="inventoryItems.length === 0" class="text-center py-12 text-slate-600">
        <p>No hay items en el inventario</p>
      </div>

      <div v-else class="bg-white rounded-xl shadow-md overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full min-w-[600px]">
            <thead class="bg-slate-50 border-b border-slate-200">
              <tr>
                <th class="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Producto
                </th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  SKU
                </th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Stock Actual
                </th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Estado
                </th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-200">
              <tr 
                v-for="item in inventoryItems" 
                :key="item.id"
                class="hover:bg-slate-50 transition-colors"
                :class="{ 'bg-warning-bg': isLowStock(item) }"
              >
                <td class="px-6 py-4 font-semibold text-slate-800">
                  {{ item.product_name || `Producto ${item.product_id}` }}
                </td>
                <td class="px-6 py-4 text-sm text-slate-600">
                  {{ item.product_sku || '-' }}
                </td>
                <td class="px-6 py-4">
                  <span 
                    class="inline-block px-3 py-1 rounded-full text-sm font-semibold"
                    :class="{
                      'bg-danger-bg text-danger': getStockClass(item) === 'out-of-stock',
                      'bg-warning-bg text-warning': getStockClass(item) === 'low-stock',
                      'bg-info-bg text-info': getStockClass(item) === 'medium-stock',
                      'bg-success-bg text-success': getStockClass(item) === 'good-stock'
                    }"
                  >
                    {{ item.quantity }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span 
                    class="inline-block px-3 py-1 rounded-full text-xs font-medium"
                    :class="{
                      'bg-danger-bg text-danger': getStockClass(item) === 'out-of-stock',
                      'bg-warning-bg text-warning': getStockClass(item) === 'low-stock',
                      'bg-info-bg text-info': getStockClass(item) === 'medium-stock',
                      'bg-success-bg text-success': getStockClass(item) === 'good-stock'
                    }"
                  >
                    {{ getStockStatus(item) }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <div class="flex space-x-2">
                    <button 
                      @click="openStockModal(item, 'increase')" 
                      class="p-2 bg-success-bg text-success hover:bg-success hover:text-white rounded-md transition-all hover:scale-110"
                      title="Aumentar stock"
                    >
                      ➕
                    </button>
                    <button 
                      @click="openStockModal(item, 'decrease')" 
                      class="p-2 bg-danger-bg text-danger hover:bg-danger hover:text-white rounded-md transition-all hover:scale-110"
                      title="Disminuir stock"
                    >
                      ➖
                    </button>
                    <button 
                      @click="openStockModal(item, 'set')" 
                      class="p-2 bg-info-bg text-info hover:bg-info hover:text-white rounded-md transition-all hover:scale-110"
                      title="Establecer stock"
                    >
                      ✏️
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div 
        v-if="showModal" 
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" 
        @click.self="closeModal"
      >
        <div class="bg-white rounded-xl w-full max-w-md">
          <div class="flex justify-between items-center p-6 border-b border-slate-200">
            <h2 class="text-2xl font-semibold text-slate-800">{{ getModalTitle() }}</h2>
            <button 
              @click="closeModal" 
              class="text-4xl text-slate-400 hover:text-slate-600 leading-none"
            >
              ×
            </button>
          </div>

          <form @submit.prevent="handleSubmit" class="p-6 space-y-5">
            <div class="bg-slate-50 p-4 rounded-lg space-y-2">
              <p class="text-slate-700">
                <strong>Producto:</strong> {{ currentItem?.product_name }}
              </p>
              <p class="text-slate-700">
                <strong>Stock Actual:</strong> {{ currentItem?.quantity }}
              </p>
            </div>

            <div class="space-y-2">
              <label class="block text-sm font-semibold text-slate-700">
                {{ getQuantityLabel() }}
              </label>
              <input
                v-model.number="quantityInput"
                type="number"
                min="0"
                required
                :disabled="submitting"
                autofocus
                class="w-full px-4 py-2 border-2 border-slate-200 rounded-lg outline-none focus:border-primary transition-colors disabled:bg-slate-50 disabled:cursor-not-allowed"
              />
            </div>

            <div v-if="modalError" class="bg-danger-bg text-danger px-4 py-3 rounded-lg text-sm text-center">
              {{ modalError }}
            </div>

            <div class="flex gap-3 pt-2">
              <button 
                type="button" 
                @click="closeModal" 
                class="flex-1 px-6 py-3 bg-slate-200 text-slate-700 font-semibold rounded-lg hover:bg-slate-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="submitting"
              >
                Cancelar
              </button>
              <button 
                type="submit" 
                class="flex-1 px-6 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="submitting"
              >
                {{ submitting ? 'Procesando...' : 'Confirmar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Layout from '../components/Layout.vue'
import { inventoryService } from '../services/inventoryService'
import { productsService } from '../services/productsService'

const inventoryItems = ref([])
const loading = ref(false)
const error = ref('')
const showModal = ref(false)
const submitting = ref(false)
const modalError = ref('')

const currentItem = ref(null)
const actionType = ref('')
const quantityInput = ref(0)

const loadInventory = async () => {
  loading.value = true
  error.value = ''

  try {
    const [inventoryResponse, productsResponse] = await Promise.all([
      inventoryService.getAll(),
      productsService.getAll().catch(() => ({ data: [] }))
    ])

    const inventory = inventoryResponse.data || inventoryResponse || []
    const products = productsResponse.data || productsResponse || []

    inventoryItems.value = inventory.map(item => {
      const product = products.find(p => p.id === item.product_id)
      return {
        ...item,
        product_name: product?.name,
        product_sku: product?.sku
      }
    })
  } catch (err) {
    error.value = 'Error al cargar el inventario'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const isLowStock = (item) => {
  return item.quantity < 10
}

const getStockClass = (item) => {
  if (item.quantity === 0) return 'out-of-stock'
  if (item.quantity < 10) return 'low-stock'
  if (item.quantity < 50) return 'medium-stock'
  return 'good-stock'
}

const getStockStatus = (item) => {
  if (item.quantity === 0) return 'Sin stock'
  if (item.quantity < 10) return 'Stock bajo'
  if (item.quantity < 50) return 'Stock medio'
  return 'Stock bueno'
}

const openStockModal = (item, type) => {
  currentItem.value = item
  actionType.value = type
  quantityInput.value = type === 'set' ? item.quantity : 0
  showModal.value = true
  modalError.value = ''
}

const closeModal = () => {
  showModal.value = false
  currentItem.value = null
  actionType.value = ''
  quantityInput.value = 0
  modalError.value = ''
}

const getModalTitle = () => {
  const titles = {
    increase: 'Aumentar Stock',
    decrease: 'Disminuir Stock',
    set: 'Establecer Stock'
  }
  return titles[actionType.value] || 'Modificar Stock'
}

const getQuantityLabel = () => {
  const labels = {
    increase: 'Cantidad a agregar',
    decrease: 'Cantidad a restar',
    set: 'Nueva cantidad'
  }
  return labels[actionType.value] || 'Cantidad'
}

const handleSubmit = async () => {
  if (quantityInput.value < 0) {
    modalError.value = 'La cantidad no puede ser negativa'
    return
  }

  if (actionType.value === 'decrease' && quantityInput.value > currentItem.value.quantity) {
    modalError.value = 'No hay suficiente stock disponible'
    return
  }

  submitting.value = true
  modalError.value = ''

  try {
    const productId = currentItem.value.product_id

    switch (actionType.value) {
      case 'increase':
        await inventoryService.increaseStock(productId, quantityInput.value)
        break
      case 'decrease':
        await inventoryService.decreaseStock(productId, quantityInput.value)
        break
      case 'set':
        await inventoryService.setStock(productId, quantityInput.value)
        break
    }

    await loadInventory()
    closeModal()
  } catch (err) {
    modalError.value = err.message || 'Error al actualizar el inventario'
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadInventory()
})
</script>
