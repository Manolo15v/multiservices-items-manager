<template>
  <Layout>
    <div class="max-w-7xl mx-auto">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold text-slate-800">Productos</h1>
        <button 
          @click="openCreateModal" 
          class="px-6 py-3 bg-gradient-to-r from-primary to-primary-dark text-white font-semibold rounded-lg hover:-translate-y-0.5 hover:shadow-lg transition-all"
        >
          ➕ Nuevo Producto
        </button>
      </div>

      <div v-if="loading" class="text-center py-12 text-slate-600">
        Cargando productos...
      </div>
      
      <div v-else-if="error" class="bg-danger-bg text-danger px-4 py-3 rounded-lg text-center">
        {{ error }}
      </div>
      
      <div v-else-if="products.length === 0" class="text-center py-12">
        <p class="text-slate-600 mb-4">No hay productos registrados</p>
        <button 
          @click="openCreateModal" 
          class="px-6 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-primary-dark transition-colors"
        >
          Crear primer producto
        </button>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="product in products" 
          :key="product.id" 
          class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg hover:-translate-y-1 transition-all"
        >
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-xl font-semibold text-slate-800">{{ product.name }}</h3>
            <div class="flex space-x-2">
              <button 
                @click="openEditModal(product)" 
                class="text-lg hover:scale-125 transition-transform" 
                title="Editar"
              >
                ✏️
              </button>
              <button 
                @click="confirmDelete(product)" 
                class="text-lg hover:scale-125 transition-transform" 
                title="Eliminar"
              >
                🗑️
              </button>
            </div>
          </div>
          <p class="text-slate-600 mb-4 line-clamp-2">{{ product.description }}</p>
          <div class="flex justify-between items-center pt-4 border-t border-slate-200">
            <span class="text-2xl font-bold text-success">${{ product.price }}</span>
            <span class="text-sm text-slate-500">SKU: {{ product.sku }}</span>
          </div>
        </div>
      </div>

      <div 
        v-if="showModal" 
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" 
        @click.self="closeModal"
      >
        <div class="bg-white rounded-xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
          <div class="flex justify-between items-center p-6 border-b border-slate-200">
            <h2 class="text-2xl font-semibold text-slate-800">
              {{ isEditing ? 'Editar Producto' : 'Nuevo Producto' }}
            </h2>
            <button 
              @click="closeModal" 
              class="text-4xl text-slate-400 hover:text-slate-600 leading-none"
            >
              ×
            </button>
          </div>
          
          <form @submit.prevent="handleSubmit" class="p-6 space-y-5">
            <div class="space-y-2">
              <label class="block text-sm font-semibold text-slate-700">Nombre</label>
              <input 
                v-model="formData.name" 
                type="text" 
                required 
                :disabled="submitting"
                class="w-full px-4 py-2 border-2 border-slate-200 rounded-lg outline-none focus:border-primary transition-colors disabled:bg-slate-50 disabled:cursor-not-allowed"
              />
            </div>

            <div class="space-y-2">
              <label class="block text-sm font-semibold text-slate-700">Descripción</label>
              <textarea 
                v-model="formData.description" 
                rows="3" 
                required 
                :disabled="submitting"
                class="w-full px-4 py-2 border-2 border-slate-200 rounded-lg outline-none focus:border-primary transition-colors resize-none disabled:bg-slate-50 disabled:cursor-not-allowed"
              ></textarea>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <label class="block text-sm font-semibold text-slate-700">Precio</label>
                <input 
                  v-model.number="formData.price" 
                  type="number" 
                  step="0.01" 
                  required 
                  :disabled="submitting"
                  class="w-full px-4 py-2 border-2 border-slate-200 rounded-lg outline-none focus:border-primary transition-colors disabled:bg-slate-50 disabled:cursor-not-allowed"
                />
              </div>

              <div class="space-y-2">
                <label class="block text-sm font-semibold text-slate-700">SKU</label>
                <input 
                  v-model="formData.sku" 
                  type="text" 
                  required 
                  :disabled="submitting"
                  class="w-full px-4 py-2 border-2 border-slate-200 rounded-lg outline-none focus:border-primary transition-colors disabled:bg-slate-50 disabled:cursor-not-allowed"
                />
              </div>
            </div>

            <div v-if="formError" class="bg-danger-bg text-danger px-4 py-3 rounded-lg text-sm text-center">
              {{ formError }}
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
                {{ submitting ? 'Guardando...' : 'Guardar' }}
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
import { productsService } from '../services/productsService'

const products = ref([])
const loading = ref(false)
const error = ref('')
const showModal = ref(false)
const isEditing = ref(false)
const submitting = ref(false)
const formError = ref('')

const formData = ref({
  id: null,
  name: '',
  description: '',
  price: 0,
  sku: ''
})

const loadProducts = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await productsService.getAll()
    products.value = response.data || response || []
  } catch (err) {
    error.value = 'Error al cargar productos'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  isEditing.value = false
  formData.value = {
    id: null,
    name: '',
    description: '',
    price: 0,
    sku: ''
  }
  showModal.value = true
}

const openEditModal = (product) => {
  isEditing.value = true
  formData.value = { ...product }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  formError.value = ''
}

const handleSubmit = async () => {
  submitting.value = true
  formError.value = ''

  try {
    if (isEditing.value) {
      await productsService.update(formData.value.id, formData.value)
    } else {
      await productsService.create(formData.value)
    }
    
    await loadProducts()
    closeModal()
  } catch (err) {
    formError.value = err.message || 'Error al guardar el producto'
  } finally {
    submitting.value = false
  }
}

const confirmDelete = async (product) => {
  if (!confirm(`¿Estás seguro de eliminar "${product.name}"?`)) return

  try {
    await productsService.delete(product.id)
    await loadProducts()
  } catch (err) {
    alert('Error al eliminar el producto')
    console.error(err)
  }
}

onMounted(() => {
  loadProducts()
})
</script>
