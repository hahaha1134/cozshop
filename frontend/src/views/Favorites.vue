<template>
  <div class="favorites">
    <div class="container">
      <h1>我的收藏</h1>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>
      
      <div v-else-if="favorites.length === 0" class="empty-state">
        <div class="empty-icon">❤️</div>
        <p>暂无收藏商品</p>
        <router-link to="/" class="btn btn-primary">去逛逛</router-link>
      </div>
      
      <div v-else class="favorites-grid">
        <div 
          v-for="favorite in favorites" 
          :key="favorite.id"
          class="favorite-card card"
        >
          <div class="product-image" @click="goToProduct(favorite.product.id)">
            <img :src="favorite.product.image" :alt="favorite.product.name" />
          </div>
          <div class="product-info">
            <h3 @click="goToProduct(favorite.product.id)">{{ favorite.product.name }}</h3>
            <p class="product-price">¥{{ favorite.product.price.toFixed(2) }}</p>
            <p class="product-stock">库存: {{ favorite.product.stock }}</p>
            <div class="product-actions">
              <button @click="removeFromFavorites(favorite.product.id)" class="btn btn-danger btn-sm">
                取消收藏
              </button>
              <button @click="addToCart(favorite.product)" class="btn btn-primary btn-sm">
                加入购物车
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { favoriteApi } from '@/utils/favoriteApi'

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()

const favorites = ref([])
const loading = ref(true)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  await fetchFavorites()
})

const fetchFavorites = async () => {
  try {
    const response = await favoriteApi.getFavorites()
    favorites.value = response
  } catch (error) {
    console.error('Failed to fetch favorites:', error)
  } finally {
    loading.value = false
  }
}

const goToProduct = (productId) => {
  router.push(`/product/${productId}`)
}

const removeFromFavorites = async (productId) => {
  try {
    await favoriteApi.removeFromFavorites(productId)
    alert('已取消收藏')
    await fetchFavorites()
  } catch (error) {
    console.error('Failed to remove from favorites:', error)
    alert('取消收藏失败')
  }
}

const addToCart = async (product) => {
  try {
    await cartStore.addToCart(product)
    alert('已添加到购物车')
  } catch (error) {
    console.error('Failed to add to cart:', error)
    alert('添加失败，请重试')
  }
}
</script>

<style scoped>
.favorites {
  padding: 40px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 2rem;
  color: var(--text-primary);
  text-align: center;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  background: var(--bg-secondary);
  border-radius: 12px;
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-top: 2rem;
}

.favorite-card {
  display: flex;
  flex-direction: column;
}

.product-image {
  height: 200px;
  overflow: hidden;
  background: var(--bg-secondary);
  cursor: pointer;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.product-image:hover img {
  transform: scale(1.05);
}

.product-info {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.product-info h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
  cursor: pointer;
  transition: color 0.3s;
}

.product-info h3:hover {
  color: var(--primary-color);
}

.product-price {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-color);
  margin: 0;
}

.product-stock {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.product-actions {
  display: flex;
  gap: 8px;
  margin-top: auto;
}

@media (max-width: 768px) {
  h1 {
    font-size: 2rem;
  }
  
  .favorites-grid {
    grid-template-columns: 1fr;
  }
}
</style>
