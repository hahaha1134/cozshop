import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const totalItems = ref(0)
  const totalPrice = ref(0)
  const loading = ref(false)
  const error = ref(null)

  const isEmpty = computed(() => items.value.length === 0)

  const fetchCart = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/cart')
      items.value = response.data.items
      totalItems.value = response.data.total_items
      totalPrice.value = response.data.total_price
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '获取购物车失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const addToCart = async (product, quantity = 1) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/cart/items', {
        product_id: product.id,
        name: product.name,
        price: product.price,
        quantity,
        image: product.image
      })
      items.value = response.data.items
      totalItems.value = response.data.total_items
      totalPrice.value = response.data.total_price
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '添加到购物车失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateQuantity = async (productId, quantity) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.put(`/cart/items/${productId}`, null, {
        params: { quantity }
      })
      items.value = response.data.items
      totalItems.value = response.data.total_items
      totalPrice.value = response.data.total_price
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '更新数量失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const removeFromCart = async (productId) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.delete(`/cart/items/${productId}`)
      items.value = response.data.items
      totalItems.value = response.data.total_items
      totalPrice.value = response.data.total_price
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '移除商品失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearCart = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.delete('/cart')
      items.value = response.data.items
      totalItems.value = response.data.total_items
      totalPrice.value = response.data.total_price
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '清空购物车失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    totalItems,
    totalPrice,
    loading,
    error,
    isEmpty,
    fetchCart,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart
  }
})