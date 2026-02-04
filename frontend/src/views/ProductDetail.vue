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
            <button 
              class="btn btn-secondary btn-lg"
              @click="toggleFavorite"
              :disabled="!authStore.isAuthenticated"
              :class="{ 'btn-danger': isFavorite }"
            >
              {{ isFavorite ? '❤️ 已收藏' : '🤍 收藏' }}
            </button>
          </div>
        </div>
      </div>
      
      <!-- Reviews Section -->
      <div class="reviews-section">
        <h2 class="reviews-title">商品评价</h2>
        
        <!-- Add Review Form -->
        <div class="add-review" v-if="authStore.isAuthenticated">
          <h3>添加评价</h3>
          <form @submit.prevent="submitReview">
            <div class="form-group">
              <label>评分</label>
              <div class="rating-input">
                <span v-for="i in 5" :key="i" class="star" @click="reviewRating = i">
                  {{ i <= reviewRating ? '★' : '☆' }}
                </span>
              </div>
            </div>
            <div class="form-group">
              <label for="review-comment">评价内容</label>
              <textarea id="review-comment" v-model="reviewComment" rows="4" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">提交评价</button>
          </form>
        </div>
        
        <!-- Reviews List -->
        <div class="reviews-list">
          <div v-if="reviews.length === 0" class="no-reviews">
            暂无评价，快来成为第一个评价的人吧！
          </div>
          <div v-for="review in reviews" :key="review.id" class="review-item">
            <div class="review-header">
              <div class="review-rating">
                <span v-for="i in 5" :key="i" class="star">
                  {{ i <= review.rating ? '★' : '☆' }}
                </span>
              </div>
              <span class="review-date">{{ formatDate(review.created_at) }}</span>
            </div>
            <div class="review-comment">{{ review.comment }}</div>
            <button v-if="authStore.isAuthenticated && review.user_id === authStore.user.id" @click="deleteReview(review.id)" class="btn btn-danger btn-sm">
              删除
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import api from '@/utils/api'
import { reviewApi } from '@/utils/reviewApi'
import { favoriteApi } from '@/utils/favoriteApi'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()

const product = ref(null)
const loading = ref(true)
const quantity = ref(1)
const reviews = ref([])
const reviewRating = ref(5)
const reviewComment = ref('')
const isFavorite = ref(false)

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

const fetchReviews = async () => {
  try {
    const response = await reviewApi.getProductReviews(route.params.id)
    reviews.value = response
  } catch (error) {
    console.error('Failed to fetch reviews:', error)
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

const submitReview = async () => {
  try {
    await reviewApi.createReview({
      product_id: route.params.id,
      rating: reviewRating.value,
      comment: reviewComment.value
    })
    alert('评价提交成功！')
    reviewRating.value = 5
    reviewComment.value = ''
    await fetchProduct() // 刷新商品信息以更新评分
    await fetchReviews() // 刷新评价列表
  } catch (error) {
    console.error('Failed to submit review:', error)
    const errorMessage = error.response?.data?.detail || '提交失败，请重试'
    alert(errorMessage)
  }
}

const deleteReview = async (reviewId) => {
  if (confirm('确定要删除这条评价吗？')) {
    try {
      await reviewApi.deleteReview(reviewId)
      alert('评价删除成功！')
      await fetchProduct() // 刷新商品信息以更新评分
      await fetchReviews() // 刷新评价列表
    } catch (error) {
      console.error('Failed to delete review:', error)
      alert('删除失败，请重试')
    }
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const checkFavoriteStatus = async () => {
  if (authStore.isAuthenticated) {
    try {
      const response = await favoriteApi.checkFavorite(route.params.id)
      isFavorite.value = response.is_favorite
    } catch (error) {
      console.error('Failed to check favorite status:', error)
    }
  }
}

const toggleFavorite = async () => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    return
  }
  
  try {
    if (isFavorite.value) {
      await favoriteApi.removeFromFavorites(route.params.id)
      isFavorite.value = false
      alert('已取消收藏')
    } else {
      await favoriteApi.addToFavorites(route.params.id)
      isFavorite.value = true
      alert('收藏成功')
    }
  } catch (error) {
    console.error('Failed to toggle favorite:', error)
    alert('操作失败，请重试')
  }
}

onMounted(() => {
  fetchProduct()
  fetchReviews()
  checkFavoriteStatus()
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

/* Reviews Section Styles */
.reviews-section {
  margin-top: 60px;
  padding-top: 40px;
  border-top: 1px solid var(--border-color);
}

.reviews-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 30px;
  color: var(--text-primary);
}

.add-review {
  background: var(--bg-secondary);
  padding: 30px;
  border-radius: 12px;
  margin-bottom: 40px;
  box-shadow: var(--shadow-sm);
}

.add-review h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: var(--text-primary);
}

.rating-input {
  display: flex;
  gap: 10px;
}

.rating-input .star {
  font-size: 24px;
  color: #ecc94b;
  cursor: pointer;
  transition: transform 0.2s;
}

.rating-input .star:hover {
  transform: scale(1.2);
}

textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  resize: vertical;
  font-family: inherit;
  font-size: 16px;
  line-height: 1.6;
}

.no-reviews {
  text-align: center;
  padding: 40px;
  background: var(--bg-secondary);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 16px;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.review-item {
  background: var(--bg-secondary);
  padding: 24px;
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.review-rating {
  display: flex;
  gap: 5px;
}

.review-rating .star {
  font-size: 16px;
  color: #ecc94b;
}

.review-date {
  font-size: 14px;
  color: var(--text-secondary);
}

.review-comment {
  line-height: 1.6;
  color: var(--text-primary);
  margin-bottom: 16px;
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
  
  .reviews-section {
    margin-top: 40px;
    padding-top: 30px;
  }
  
  .add-review {
    padding: 20px;
  }
  
  .review-item {
    padding: 20px;
  }
}
</style>