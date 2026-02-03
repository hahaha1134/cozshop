<template>
  <div class="product-detail">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
    </div>
    
    <div v-else-if="!product" class="empty-state">
      <div class="empty-state-icon">📦</div>
      <p class="empty-state-text">商品不存在</p>
      <router-link to="/" class="btn btn-primary">返回首页</router-link>
    </div>
    
    <div v-else class="container">
      <div class="product-content">
        <div class="product-image-section">
          <img :src="product.image" :alt="product.name" class="product-image" />
        </div>
        
        <div class="product-details">
          <h1 class="product-title">{{ product.name }}</h1>
          <p class="product-category">{{ product.category }}</p>
          
          <div class="product-rating">
            <span class="stars">⭐</span>
            <span>{{ product.rating }}</span>
            <span class="reviews">({{ product.numReviews }} 评价)</span>
          </div>
          
          <div class="product-price-section">
            <span class="product-price">¥{{ product.price.toFixed(2) }}</span>
            <span class="stock-status" :class="{ 'in-stock': product.stock > 0, 'out-of-stock': product.stock === 0 }">
              {{ product.stock > 0 ? `库存: ${product.stock}` : '暂时缺货' }}
            </span>
          </div>
          
          <p class="product-description">{{ product.description }}</p>
          
          <div class="quantity-selector">
            <label>数量:</label>
            <div class="quantity-controls">
              <button 
                class="btn btn-secondary btn-sm"
                @click="quantity = Math.max(1, quantity - 1)"
                :disabled="quantity <= 1"
              >-</button>
              <span class="quantity-value">{{ quantity }}</span>
              <button 
                class="btn btn-secondary btn-sm"
                @click="quantity = Math.min(product.stock, quantity + 1)"
                :disabled="quantity >= product.stock"
              >+</button>
            </div>
          </div>
          
          <div class="product-actions">
            <button 
              class="btn btn-primary btn-lg"
              @click="addToCart"
              :disabled="!authStore.isAuthenticated || product.stock === 0"
            >
              {{ authStore.isAuthenticated ? '加入购物车' : '请先登录' }}
            </button>
            <router-link to="/" class="btn btn-secondary btn-lg">返回首页</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import api from '@/utils/api'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()

const product = ref(null)
const loading = ref(true)
const quantity = ref(1)

const fetchProduct = async () => {
  try {
    const response = await api.get(`/products/${route.params.id}`)
    product.value = response.data
  } catch (error) {
    console.error('Failed to fetch product:', error)
  } finally {
    loading.value = false
  }
}

const addToCart = async () => {
  try {
    await cartStore.addToCart(product.value, quantity.value)
    alert('已添加到购物车！')
  } catch (error) {
    console.error('Failed to add to cart:', error)
    alert('添加失败，请重试')
  }
}

onMounted(() => {
  fetchProduct()
})
</script>

<style scoped>
.product-detail {
  padding: 40px 0;
}

.product-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: start;
}

.product-image-section {
  position: sticky;
  top: 100px;
}

.product-image {
  width: 100%;
  border-radius: 12px;
  box-shadow: var(--shadow-lg);
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.product-title {
  font-size: 36px;
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
}

.product-category {
  font-size: 14px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.product-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
}

.stars {
  font-size: 20px;
  color: #ecc94b;
}

.reviews {
  color: var(--text-secondary);
}

.product-price-section {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 0;
  border-top: 1px solid var(--border-color);
  border-bottom: 1px solid var(--border-color);
}

.product-price {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary-color);
}

.stock-status {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.stock-status.in-stock {
  background: #c6f6d5;
  color: #22543d;
}

.stock-status.out-of-stock {
  background: #fed7d7;
  color: #742a2a;
}

.product-description {
  font-size: 16px;
  line-height: 1.8;
  color: var(--text-primary);
  margin: 0;
}

.quantity-selector {
  display: flex;
  align-items: center;
  gap: 16px;
}

.quantity-selector label {
  font-weight: 600;
  color: var(--text-primary);
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.quantity-value {
  min-width: 40px;
  text-align: center;
  font-weight: 600;
  font-size: 16px;
}

.product-actions {
  display: flex;
  gap: 16px;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .product-content {
    grid-template-columns: 1fr;
  }
  
  .product-image-section {
    position: static;
  }
  
  .product-title {
    font-size: 24px;
  }
  
  .product-price {
    font-size: 24px;
  }
  
  .product-actions {
    flex-direction: column;
  }
}
</style>