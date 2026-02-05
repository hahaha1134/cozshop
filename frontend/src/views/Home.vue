<template>
  <div class="home">
    <div class="hero">
      <div class="container">
        <h1 class="hero-title">欢迎来到 CozShop</h1>
        <p class="hero-subtitle">发现优质商品，享受购物乐趣</p>
        
        <!-- Search Bar -->
        <div class="search-bar">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="搜索商品..."
            class="search-input"
          />
          <button @click="fetchProducts" class="search-btn">搜索</button>
        </div>
      </div>
    </div>
    
    <!-- Announcements -->
    <div class="announcements-section">
      <div class="container">
        <h2 class="section-title">系统公告</h2>
        <div v-if="announcements.length > 0" class="announcements-list">
          <div v-for="announcement in announcements" :key="announcement.id" class="announcement-item">
            <h3 class="announcement-title">{{ announcement.title }}</h3>
            <p class="announcement-content">{{ announcement.content }}</p>
            <span class="announcement-date">{{ formatDate(announcement.created_at) }}</span>
          </div>
        </div>
        <div v-else class="empty-announcements">
          <p>暂无系统公告</p>
        </div>
      </div>
    </div>
    
    <div class="container">
      <!-- Filters -->
      <div class="filters-container">
        <div class="category-filters">
          <button 
            v-for="category in categories" 
            :key="category"
            @click="selectedCategory = category; fetchProducts()"
            :class="['filter-btn', { active: selectedCategory === category }]"
          >
            {{ category }}
          </button>
        </div>
        
        <!-- Price Filter -->
        <div class="price-filter">
          <label>价格范围:</label>
          <div class="price-inputs">
            <input 
              type="number" 
              v-model.number="minPrice" 
              placeholder="最低"
              min="0"
              step="0.01"
              class="price-input"
            />
            <span>-</span>
            <input 
              type="number" 
              v-model.number="maxPrice" 
              placeholder="最高"
              min="0"
              step="0.01"
              class="price-input"
            />
            <button @click="fetchProducts" class="btn btn-sm btn-primary">筛选</button>
          </div>
        </div>
      </div>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="products.length === 0" class="empty-state">
        <div class="empty-state-icon">📦</div>
        <p class="empty-state-text">暂无商品</p>
      </div>
      
      <div v-else class="products-grid">
        <div 
          v-for="product in products" 
          :key="product.id"
          class="product-card card"
          @click="goToProduct(product.id)"
        >
          <div class="product-image">
            <img 
              :src="product.image || 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDMwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjZjBmMGMwIi8+CjxwYXRoIGQ9Ik0xNTAgMTUwIEMxNzcuNjEgMTUwIDE5NSAxMzIuNjEgMTk1IDEwNSBDMTk1IDc3LjM5IDE3Ny42MSA2MCAxNTAgNjAgQzEyMi4zOSA2MCAxMDUgNzcuMzkgMTA1IDEwNSBDMTA1IDEzMi42MSAxMjIuMzkgMTUwIDE1MCAxNTAiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTE1IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiMwMDAiPk5vIEltYWdlPC90ZXh0Pgo8L3N2Zz4='" 
              :alt="product.name"
              @error="$event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDMwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjZjBmMGMwIi8+CjxwYXRoIGQ9Ik0xNTAgMTUwIEMxNzcuNjEgMTUwIDE5NSAxMzIuNjEgMTk1IDEwNSBDMTk1IDc3LjM5IDE3Ny42MSA2MCAxNTAgNjAgQzEyMi4zOSA2MCAxMDUgNzcuMzkgMTA1IDEwNSBDMTA1IDEzMi42MSAxMjIuMzkgMTUwIDE1MCAxNTAiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTE1IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiMwMDAiPk5vIEltYWdlPC90ZXh0Pgo8L3N2Zz4='"
            />
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
const searchQuery = ref('')
const minPrice = ref(null)
const maxPrice = ref(null)
const announcements = ref([])

const fetchProducts = async () => {
  loading.value = true
  try {
    console.log('Fetching products with params:', {
      search: searchQuery.value,
      category: selectedCategory.value,
      min_price: minPrice.value,
      max_price: maxPrice.value
    })
    // Build query params
    const params = {}
    
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    
    if (selectedCategory.value !== '全部') {
      params.category = selectedCategory.value
    }
    
    if (minPrice.value !== null && minPrice.value > 0) {
      params.min_price = minPrice.value
    }
    
    if (maxPrice.value !== null && maxPrice.value > 0) {
      params.max_price = maxPrice.value
    }
    
    const response = await api.get('/products', { params })
    console.log('Products fetched:', response.data.length)
    console.log('First product:', response.data[0])
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

onMounted(async () => {
  await fetchProducts()
  await fetchAnnouncements()
})

const fetchAnnouncements = async () => {
  try {
    const response = await api.get('/system/announcements/public')
    announcements.value = response.data
  } catch (error) {
    console.error('Failed to fetch announcements:', error)
    // 静默失败，因为公告不是必须的
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
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

.announcements-section {
  background: #f9f9f9;
  padding: 40px 0;
  margin-bottom: 40px;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 24px;
  color: var(--text-primary);
  text-align: center;
}

.announcements-list {
  max-width: 800px;
  margin: 0 auto;
}

.announcement-item {
  background: white;
  padding: 24px;
  margin-bottom: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.announcement-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.announcement-content {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 12px;
  line-height: 1.5;
}

.announcement-date {
  font-size: 12px;
  color: var(--text-tertiary);
}

.empty-announcements {
  text-align: center;
  padding: 40px 0;
  color: var(--text-secondary);
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 16px;
}

.hero-subtitle {
  font-size: 20px;
  opacity: 0.9;
  margin-bottom: 32px;
}

/* Search Bar */
.search-bar {
  display: flex;
  max-width: 600px;
  margin: 0 auto;
  gap: 8px;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  outline: none;
}

.search-btn {
  padding: 12px 24px;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.search-btn:hover {
  background: #f0f0f0;
}

/* Filters */
.filters-container {
  margin-bottom: 32px;
}

.category-filters {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
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

/* Price Filter */
.price-filter {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  background: var(--bg-secondary);
  padding: 16px;
  border-radius: 8px;
}

.price-filter label {
  font-weight: 600;
  color: var(--text-primary);
}

.price-inputs {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.price-input {
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  width: 100px;
  font-size: 14px;
}

.price-input:focus {
  outline: none;
  border-color: var(--primary-color);
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
  display: -moz-box;
  display: box;
  -webkit-line-clamp: 2;
  -moz-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  -moz-box-orient: vertical;
  box-orient: vertical;
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