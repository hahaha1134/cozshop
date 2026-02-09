<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>个人中心</h1>
      <p class="welcome-text">欢迎，{{ authStore.user?.name || authStore.user?.username }}</p>
    </div>

    <div class="profile-content">
      <!-- 个人资料 -->
      <div class="profile-section">
        <h2>1. 个人资料</h2>
        <div class="info-grid">
          <div class="info-item">
            <label>用户名</label>
            <span>{{ authStore.user?.name || authStore.user?.username }}</span>
          </div>
          <div class="info-item">
            <label>邮箱</label>
            <span>{{ authStore.user?.email }}</span>
          </div>
          <div class="info-item">
            <label>手机号</label>
            <span>{{ authStore.user?.phone || '未设置' }}</span>
          </div>
          <div class="info-item">
            <label>收货地址</label>
            <span>{{ authStore.user?.address || '未设置' }}</span>
          </div>
          <div class="info-item">
            <label>注册时间</label>
            <span>{{ formatDate(authStore.user?.created_at) }}</span>
          </div>
        </div>

        <div class="update-form">
          <h3>修改个人信息</h3>
          <div class="form-group">
            <label for="name">用户名</label>
            <input 
              type="text" 
              id="name" 
              v-model="updateForm.name" 
              placeholder="请输入用户名"
            >
          </div>
          <div class="form-group">
            <label for="phone">手机号</label>
            <input 
              type="tel" 
              id="phone" 
              v-model="updateForm.phone" 
              placeholder="请输入手机号"
            >
          </div>
          <div class="form-group">
            <label for="address">收货地址</label>
            <textarea 
              id="address" 
              v-model="updateForm.address" 
              placeholder="请输入收货地址"
              rows="3"
            ></textarea>
          </div>
          <div class="form-actions">
            <button 
              @click="updateProfile" 
              class="update-btn"
              :disabled="isUpdating"
            >
              {{ isUpdating ? '更新中...' : '更新信息' }}
            </button>
          </div>
          <div v-if="message" class="message" :class="messageType">
            {{ message }}
          </div>
        </div>
      </div>

      <!-- 我的商品 -->
      <div class="profile-section">
        <h2>2. 我的商品</h2>
        <div class="product-filters">
          <button 
            v-for="status in productStatuses" 
            :key="status.value"
            @click="selectedProductStatus = status.value"
            :class="['btn', 'btn-sm', selectedProductStatus === status.value ? 'btn-primary' : 'btn-secondary']"
          >
            {{ status.label }}
          </button>
        </div>
        <div v-if="loadingProducts" class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
        <div v-else-if="filteredProducts.length === 0" class="empty-state">
          <div class="empty-icon">📦</div>
          <p>暂无商品</p>
          <router-link to="/product/create" class="btn btn-primary">发布新商品</router-link>
        </div>
        <div v-else class="products-grid">
          <div v-for="product in filteredProducts" :key="product.id" class="product-card">
            <div class="product-image">
              <img 
                :src="product.image" 
                :alt="product.name"
                @error="$event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjZjBmMGMwIi8+CjxwYXRoIGQ9Ik0xNTAgMTUwIEMxNzcuNjEgMTUwIDE5NSAxMzIuNjEgMTk1IDEwNSBDMTk1IDc3LjM5IDE3Ny42MSA2MCAxNTAgNjAgQzEyMi4zOSA2MCAxMDUgNzcuMzkgMTA1IDEwNSBDMTA1IDEzMi42MSAxMjIuMzkgMTUwIDE1MCAxNTAiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTY1IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiMwMDAiPk5vIEltYWdlPC90ZXh0Pgo8L3N2Zz4='" 
              >
            </div>
            <div class="product-info">
              <h3>{{ product.name }}</h3>
              <p class="product-price">¥{{ product.price.toFixed(2) }}</p>
              <p class="product-stock">库存: {{ product.stock }}</p>
              <p class="product-status">
                状态: <span :class="['status-badge', `status-${product.status || 'pending'}`]">
                  {{ getProductStatusText(product.status || 'pending') }}
                </span>
              </p>
              <div class="product-actions">
                <router-link :to="`/product/edit/${product.id}`" class="btn btn-primary btn-sm">
                  编辑
                </router-link>
                <button @click="toggleProductStatus(product.id, product.status !== 'active')" class="btn btn-warning btn-sm">
                  {{ product.status === 'active' ? '下架' : '上架' }}
                </button>
                <button @click="deleteProduct(product.id)" class="btn btn-danger btn-sm">
                  删除
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 我的订单 -->
      <div class="profile-section">
        <h2>3. 我的订单</h2>
        <div class="order-filters">
          <button 
            v-for="status in orderStatuses" 
            :key="status.value"
            @click="selectedOrderStatus = status.value"
            :class="['btn', 'btn-sm', selectedOrderStatus === status.value ? 'btn-primary' : 'btn-secondary']"
          >
            {{ status.label }}
          </button>
        </div>
        <div v-if="loadingOrders" class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
        <div v-else-if="filteredOrders.length === 0" class="empty-state">
          <div class="empty-icon">📋</div>
          <p>暂无订单</p>
          <router-link to="/" class="btn btn-primary">去购物</router-link>
        </div>
        <div v-else class="orders-list">
          <div 
            v-for="order in filteredOrders" 
            :key="order.id"
            class="order-card"
          >
            <div class="order-header">
              <div class="order-info">
                <span class="order-id">订单号: {{ order.id }}</span>
                <span class="order-date">{{ formatDate(order.created_at) }}</span>
              </div>
              <span :class="['order-status', `status-${order.status}`]">
                {{ getOrderStatusText(order.status) }}
              </span>
            </div>
            <div class="order-items">
              <div 
                v-for="item in order.orderItems" 
                :key="item.product_id"
                class="order-item"
              >
                <img 
                  :src="item.image || 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIiBmaWxsPSIjZjBmMGMwIi8+CjxwYXRoIGQ9Ik01MCA1MCBDNzcuNjEgNTAgMTAwIDIyLjYxIDEwMCAwIEMxMDAgMCA3Ny42MSAwIDUwIDAgQzIyLjM5IDAgMCAyMi42MSAwIDUwIEMwIDc3LjYxIDIyLjM5IDEwMCA1MCAxMDAiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEwIiBmaWxsPSIjMDAwIj5ObyBJbmMGMwIi8+CjxwYXRoIGQ9Ik0xNTAgMTUwIEMxNzcuNjEgMTUwIDE5NSAxMzIuNjEgMTk1IDEwNSBDMTk1IDc3LjM5IDE3Ny42MSA2MCAxNTAgNjAgQzEyMi4zOSA2MCAxMDUgNzcuMzkgMTA1IDEwNSBDMTA1IDEzMi42MSAxMjIuMzkgMTUwIDE1MCAxNTAiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTE1IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiMwMDAiPk5vIEltYWdlPC90ZXh0Pgo8L3N2Zz4='" 
                  :alt="item.name" 
                  class="item-image"
                />
                <div class="item-details">
                  <h4 class="item-name">{{ item.name }}</h4>
                  <p class="item-price">¥{{ item.price.toFixed(2) }} × {{ item.quantity }}</p>
                </div>
                <span class="item-total">¥{{ (item.price * item.quantity).toFixed(2) }}</span>
              </div>
            </div>
            <div class="order-footer">
              <div class="order-total">
                <span>订单总计:</span>
                <span>¥{{ order.totalPrice.toFixed(2) }}</span>
              </div>
              <div class="order-actions">
                <button class="btn btn-secondary btn-sm">查看详情</button>
                <button v-if="order.status === 'pending'" class="btn btn-danger btn-sm">取消订单</button>
                <button v-if="order.status === 'shipped'" class="btn btn-success btn-sm">确认收货</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 我的收藏 -->
      <div class="profile-section">
        <h2>4. 我的收藏</h2>
        <div v-if="loadingFavorites" class="loading">
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
            class="favorite-card"
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

      <!-- 安全设置 -->
      <div class="profile-section">
        <h2>5. 安全设置</h2>
        <div class="update-form">
          <h3>修改登录密码</h3>
          <div class="form-group">
            <label for="oldPassword">旧密码</label>
            <input 
              type="password" 
              id="oldPassword" 
              v-model="passwordForm.oldPassword" 
              placeholder="请输入旧密码"
            >
          </div>
          <div class="form-group">
            <label for="newPassword">新密码</label>
            <input 
              type="password" 
              id="newPassword" 
              v-model="passwordForm.newPassword" 
              placeholder="请输入新密码"
            >
          </div>
          <div class="form-group">
            <label for="confirmPassword">确认新密码</label>
            <input 
              type="password" 
              id="confirmPassword" 
              v-model="passwordForm.confirmPassword" 
              placeholder="请确认新密码"
            >
          </div>
          <div class="form-actions">
            <button 
              @click="updatePassword" 
              class="update-btn"
              :disabled="isUpdatingPassword"
            >
              {{ isUpdatingPassword ? '更新中...' : '修改密码' }}
            </button>
          </div>
          <div v-if="passwordMessage" class="message" :class="passwordMessageType">
            {{ passwordMessage }}
          </div>
        </div>
      </div>

      <!-- 我的评价 -->
      <div class="profile-section">
        <h2>6. 我的评价</h2>
        <div v-if="loadingReviews" class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
        <div v-else-if="reviews.length === 0" class="empty-state">
          <div class="empty-icon">⭐</div>
          <p>暂无评价</p>
        </div>
        <div v-else class="reviews-list">
          <div 
            v-for="review in reviews" 
            :key="review.id"
            class="review-card"
          >
            <div class="review-header">
              <span class="review-product">{{ review.product_name }}</span>
              <span class="review-rating">
                {{ '★'.repeat(review.rating) }}{{ '☆'.repeat(5 - review.rating) }}
              </span>
            </div>
            <div class="review-content">
              <p>{{ review.comment }}</p>
            </div>
            <div class="review-footer">
              <span class="review-date">{{ formatDate(review.created_at) }}</span>
              <button class="btn btn-secondary btn-sm">查看订单</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useRouter } from 'vue-router'
import api from '@/utils/api'
import { favoriteApi } from '@/utils/favoriteApi'

const authStore = useAuthStore()
const cartStore = useCartStore()
const router = useRouter()

// 个人资料表单
const updateForm = ref({
  name: '',
  phone: '',
  address: ''
})
const isUpdating = ref(false)
const message = ref('')
const messageType = ref('')

// 密码修改表单
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const isUpdatingPassword = ref(false)
const passwordMessage = ref('')
const passwordMessageType = ref('')

// 商品管理
const products = ref([])
const loadingProducts = ref(false)
const selectedProductStatus = ref('all')
const productStatuses = [
  { value: 'all', label: '全部' },
  { value: 'pending', label: '审核中' },
  { value: 'approved', label: '已上架' },
  { value: 'inactive', label: '已下架' }
]

// 订单管理
const orders = ref([])
const loadingOrders = ref(false)
const selectedOrderStatus = ref('all')
const orderStatuses = [
  { value: 'all', label: '全部' },
  { value: 'pending', label: '待付款' },
  { value: 'processing', label: '待发货' },
  { value: 'shipped', label: '待收货' },
  { value: 'delivered', label: '已完成' },
  { value: 'cancelled', label: '已取消' }
]

// 收藏管理
const favorites = ref([])
const loadingFavorites = ref(false)

// 评价管理
const reviews = ref([])
const loadingReviews = ref(false)

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 筛选商品
const filteredProducts = computed(() => {
  if (selectedProductStatus.value === 'all') {
    return products.value
  }
  return products.value.filter(product => product.status === selectedProductStatus.value)
})

// 筛选订单
const filteredOrders = computed(() => {
  if (selectedOrderStatus.value === 'all') {
    return orders.value
  }
  return orders.value.filter(order => order.status === selectedOrderStatus.value)
})

// 获取商品状态文本
const getProductStatusText = (status) => {
  const statusMap = {
    pending: '审核中',
    approved: '已上架',
    inactive: '已下架',
    rejected: '已驳回'
  }
  return statusMap[status] || '未知'
}

// 获取订单状态文本
const getOrderStatusText = (status) => {
  const statusMap = {
    pending: '待付款',
    processing: '待发货',
    shipped: '待收货',
    delivered: '已完成',
    cancelled: '已取消'
  }
  return statusMap[status] || status
}

// 更新个人资料
const updateProfile = async () => {
  try {
    isUpdating.value = true
    message.value = ''
    
    const response = await api.put('/users/profile/update', {
      name: updateForm.value.name || undefined,
      phone: updateForm.value.phone || undefined,
      address: updateForm.value.address || undefined
    })
    
    message.value = response.data.message
    messageType.value = 'success'
    
    // 更新用户信息
    if (response.data.user) {
      authStore.updateUser(response.data.user)
    }
    
    // 重置表单
    updateForm.value = {
      name: '',
      phone: '',
      address: ''
    }
    
  } catch (error) {
    console.error('Update profile failed:', error)
    message.value = error.response?.data?.detail || '更新失败，请重试'
    messageType.value = 'error'
  } finally {
    isUpdating.value = false
  }
}

// 更新密码
const updatePassword = async () => {
  try {
    isUpdatingPassword.value = true
    passwordMessage.value = ''
    
    if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
      passwordMessage.value = '两次输入的密码不一致'
      passwordMessageType.value = 'error'
      return
    }
    
    // 这里需要实现密码修改的API调用
    // 由于后端暂时没有实现密码修改接口，这里只做前端验证
    passwordMessage.value = '密码修改功能暂未实现'
    passwordMessageType.value = 'info'
    
    // 重置表单
    passwordForm.value = {
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
    
  } catch (error) {
    console.error('Update password failed:', error)
    passwordMessage.value = error.response?.data?.detail || '修改失败，请重试'
    passwordMessageType.value = 'error'
  } finally {
    isUpdatingPassword.value = false
  }
}

// 获取我的商品
const fetchProducts = async () => {
  try {
    loadingProducts.value = true
    const response = await api.get('/products/my')
    products.value = response.data
  } catch (error) {
    console.error('Fetch products failed:', error)
  } finally {
    loadingProducts.value = false
  }
}

// 切换商品状态
const toggleProductStatus = async (productId, newStatus) => {
  try {
    const status = newStatus ? 'approved' : 'inactive'
    await api.put(`/products/${productId}/status`, { status })
    
    // 更新本地状态
    const product = products.value.find(p => p.id === productId)
    if (product) {
      product.status = status
    }
  } catch (error) {
    console.error('Toggle product status failed:', error)
    alert('更新商品状态失败')
  }
}

// 删除商品
const deleteProduct = async (productId) => {
  if (confirm('确定要删除这个商品吗？')) {
    try {
      await api.delete(`/products/${productId}`)
      products.value = products.value.filter(p => p.id !== productId)
      alert('商品删除成功！')
    } catch (error) {
      console.error('Delete product failed:', error)
      alert('删除失败，请重试')
    }
  }
}

// 获取我的订单
const fetchOrders = async () => {
  try {
    loadingOrders.value = true
    const response = await api.get('/orders')
    orders.value = response.data
  } catch (error) {
    console.error('Fetch orders failed:', error)
  } finally {
    loadingOrders.value = false
  }
}

// 获取我的收藏
const fetchFavorites = async () => {
  try {
    loadingFavorites.value = true
    const response = await favoriteApi.getFavorites()
    favorites.value = response
  } catch (error) {
    console.error('Fetch favorites failed:', error)
  } finally {
    loadingFavorites.value = false
  }
}

// 移除收藏
const removeFromFavorites = async (productId) => {
  try {
    await favoriteApi.removeFromFavorites(productId)
    favorites.value = favorites.value.filter(f => f.product.id !== productId)
    alert('已取消收藏')
  } catch (error) {
    console.error('Remove from favorites failed:', error)
    alert('取消收藏失败')
  }
}

// 加入购物车
const addToCart = async (product) => {
  try {
    await cartStore.addToCart(product)
    alert('已添加到购物车')
  } catch (error) {
    console.error('Add to cart failed:', error)
    alert('添加失败，请重试')
  }
}

// 跳转到商品详情
const goToProduct = (productId) => {
  router.push(`/product/${productId}`)
}

// 获取我的评价
const fetchReviews = async () => {
  try {
    loadingReviews.value = true
    // 这里需要实现获取评价的API调用
    // 由于后端暂时没有实现评价列表接口，这里只做模拟数据
    reviews.value = []
  } catch (error) {
    console.error('Fetch reviews failed:', error)
  } finally {
    loadingReviews.value = false
  }
}

// 初始化数据
onMounted(async () => {
  // 初始化个人资料表单
  if (authStore.user) {
    updateForm.value.name = authStore.user.name || ''
    updateForm.value.phone = authStore.user.phone || ''
    updateForm.value.address = authStore.user.address || ''
  }
  
  // 获取数据
  await Promise.all([
    fetchProducts(),
    fetchOrders(),
    fetchFavorites(),
    fetchReviews()
  ])
})
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.profile-header {
  margin-bottom: 2rem;
}

.profile-header h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.welcome-text {
  color: #666;
  font-size: 1.1rem;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-section h2 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #4CAF50;
}

.profile-section h3 {
  font-size: 1.2rem;
  color: #555;
  margin: 1rem 0;
}

/* 信息网格 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item label {
  font-weight: 600;
  color: #666;
  font-size: 0.9rem;
}

.info-item span {
  color: #333;
  font-size: 1.1rem;
}

/* 表单样式 */
.update-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #666;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.update-btn {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.update-btn:hover {
  background: #45a049;
}

.update-btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

/* 消息样式 */
.message {
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.message.success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.message.info {
  background: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}

/* 筛选按钮 */
.product-filters,
.order-filters {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

/* 加载状态 */
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
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  background: #f8f9fa;
  border-radius: 8px;
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

/* 商品网格 */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.product-card {
  background: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.product-image {
  height: 200px;
  overflow: hidden;
  background: #e9ecef;
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
  padding: 1.5rem;
}

.product-info h3 {
  font-size: 1.2rem;
  margin: 0 0 0.5rem 0;
  color: #333;
}

.product-price {
  font-size: 1.1rem;
  font-weight: 700;
  color: #4CAF50;
  margin: 0 0 0.5rem 0;
}

.product-stock {
  font-size: 0.9rem;
  color: #666;
  margin: 0 0 0.5rem 0;
}

.product-status {
  font-size: 0.9rem;
  margin: 0 0 1rem 0;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-pending {
  background: #feebc8;
  color: #744210;
}

.status-approved {
  background: #c6f6d5;
  color: #22543d;
}

.status-inactive {
  background: #fed7d7;
  color: #742a2a;
}

.status-rejected {
  background: #fed7d7;
  color: #742a2a;
}

.product-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

/* 订单样式 */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.order-card {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  overflow: hidden;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.order-id {
  font-weight: 600;
  color: #333;
}

.order-date {
  font-size: 0.9rem;
  color: #666;
}

.order-status {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
}

.status-pending {
  background: #feebc8;
  color: #744210;
}

.status-processing {
  background: #bee3f8;
  color: #2a4365;
}

.status-shipped {
  background: #c6f6d5;
  color: #22543d;
}

.status-delivered {
  background: #9ae6b4;
  color: #22543d;
}

.status-cancelled {
  background: #fed7d7;
  color: #742a2a;
}

.order-items {
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f1f3f5;
}

.order-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.item-details {
  flex: 1;
}

.item-name {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
  color: #333;
}

.item-price {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
}

.item-total {
  font-weight: 600;
  color: #333;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
}

.order-total {
  font-size: 1.1rem;
  font-weight: 700;
}

.order-total span:last-child {
  color: #4CAF50;
  margin-left: 0.5rem;
}

.order-actions {
  display: flex;
  gap: 0.5rem;
}

/* 收藏样式 */
.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.favorite-card {
  background: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.favorite-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 评价样式 */
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.review-card {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.review-product {
  font-weight: 600;
  color: #333;
}

.review-rating {
  color: #ffc107;
  font-size: 1.1rem;
}

.review-content {
  margin-bottom: 1rem;
}

.review-content p {
  color: #555;
  line-height: 1.5;
}

.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #666;
}

/* 按钮样式 */
.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-sm {
  padding: 0.25rem 0.75rem;
  font-size: 0.8rem;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.btn-warning {
  background-color: #ffc107;
  color: #212529;
}

.btn-warning:hover {
  background-color: #e0a800;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-success:hover {
  background-color: #218838;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .profile-container {
    padding: 1rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .products-grid,
  .favorites-grid {
    grid-template-columns: 1fr;
  }
  
  .product-filters,
  .order-filters {
    flex-direction: column;
  }
  
  .order-header,
  .order-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .order-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .product-actions {
    flex-direction: column;
  }
  
  .order-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .order-actions .btn {
    width: 100%;
  }
}
</style>