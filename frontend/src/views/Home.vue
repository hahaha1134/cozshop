<template>
  <div class="home">
    <div class="hero">
      <div class="container">
        <h1 class="hero-title">欢迎来到 CozShop</h1>
        <p class="hero-subtitle">发现优质商品，享受购物乐趣</p>
      </div>
    </div>
    
    <div class="container">
      <div class="filters">
        <button 
          v-for="category in categories" 
          :key="category"
          @click="selectedCategory = category"
          :class="['filter-btn', { active: selectedCategory === category }]"
        >
          {{ category }}
        </button>
      </div>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="filteredProducts.length === 0" class="empty-state">
        <div class="empty-state-icon">📦</div>
        <p class="empty-state-text">暂无商品</p>
      </div>
      
      <div v-else class="products-grid">
        <div 
          v-for="product in filteredProducts" 
          :key="product.id"
          class="product-card card"
          @click="goToProduct(product.id)"
        >
          <div class="product-image">
            <img :src="product.image" :alt="product.name" />
          </div>
          <div class="product-info">
            <h3 class="product-name">{{ product.name }}</h3>
            <p class="product-description">{{ product.description }}</p>
            <div class="product-meta">
              <span class="product-price">¥{{ product.price.toFixed(2) }}</span>
              <span class="product-category">{{ product.category }}</span>
            </div>
            <div class="product-rating">
              <span class="stars">⭐</span>
              <span>{{ product.rating }}</span>
              <span class="reviews">({{ product.numReviews }} 评价)</span>
            </div>
            <button 
              class="btn btn-primary btn-sm"
              @click.stop="addToCart(product)"
              :disabled="!authStore.isAuthenticated"
            >
              {{ authStore.isAuthenticated ? '加入购物车' : '请先登录' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import api from '@/utils/api'

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()

const products = ref([])
const loading = ref(true)
const selectedCategory = ref('全部')
const categories = ref(['全部', 'Electronics', 'Accessories'])

const filteredProducts = computed(() => {
  if (selectedCategory.value === '全部') {
    return products.value
  }
  return products.value.filter(p => p.category === selectedCategory.value)
})

const fetchProducts = async () => {
  try {
    const response = await api.get('/products')
    products.value = response.data
  } catch (error) {
    console.error('Failed to fetch products:', error)
  } finally {
    loading.value = false
  }
}

const goToProduct = (id) => {
  router.push(`/product/${id}`)
}

const addToCart = async (product) => {
  try {
    await cartStore.addToCart(product)
    alert('已添加到购物车！')
  } catch (error) {
    console.error('Failed to add to cart:', error)
    alert('添加失败，请重试')
  }
}

onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.home {
  min-height: 100vh;
}

.hero {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 60px 0;
  text-align: center;
  margin-bottom: 40px;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 16px;
}

.hero-subtitle {
  font-size: 20px;
  opacity: 0.9;
}

.filters {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 8px 20px;
  border: 2px solid var(--border-color);
  border-radius: 20px;
  background: white;
  color: var(--text-primary);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.filter-btn.active {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.product-card {
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.product-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: var(--bg-secondary);
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.product-name {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.product-description {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-price {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-color);
}

.product-category {
  font-size: 12px;
  padding: 4px 12px;
  background: var(--bg-secondary);
  border-radius: 12px;
  color: var(--text-secondary);
}

.product-rating {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: var(--text-secondary);
}

.stars {
  color: #ecc94b;
}

.reviews {
  font-size: 12px;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 32px;
  }
  
  .hero-subtitle {
    font-size: 16px;
  }
  
  .products-grid {
    grid-template-columns: 1fr;
  }
}
</style>