<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>个人中心</h1>
      <p class="welcome-text">欢迎，{{ authStore.user?.name || authStore.user?.username }}</p>
    </div>

    <div class="profile-content">
      <div class="profile-section">
        <h2>个人信息</h2>
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
      </div>

      <div class="profile-section">
        <h2>修改个人信息</h2>
        <div class="update-form">
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

      <div class="profile-section">
        <h2>快捷操作</h2>
        <div class="quick-actions">
          <router-link to="/orders" class="action-card">
            <div class="action-icon">📦</div>
            <div class="action-text">
              <h3>我的订单</h3>
              <p>查看订单历史</p>
            </div>
          </router-link>
          <router-link to="/cart" class="action-card">
            <div class="action-icon">🛒</div>
            <div class="action-text">
              <h3>购物车</h3>
              <p>管理购物车商品</p>
            </div>
          </router-link>
          <router-link to="/product/manage" class="action-card">
            <div class="action-icon">📋</div>
            <div class="action-text">
              <h3>我的商品</h3>
              <p>管理发布的商品</p>
            </div>
          </router-link>
          <router-link to="/product/create" class="action-card">
            <div class="action-icon">➕</div>
            <div class="action-text">
              <h3>发布商品</h3>
              <p>发布二手商品</p>
            </div>
          </router-link>
          <router-link to="/favorites" class="action-card">
            <div class="action-icon">❤️</div>
            <div class="action-text">
              <h3>我的收藏</h3>
              <p>查看收藏商品</p>
            </div>
          </router-link>
        </div>
      </div>

      <div class="profile-section">
        <h2>账户设置</h2>
        <button @click="handleLogout" class="logout-btn">退出登录</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/utils/api'

const authStore = useAuthStore()
const router = useRouter()

// Form state
const updateForm = ref({
  name: '',
  phone: '',
  address: ''
})
const isUpdating = ref(false)
const message = ref('')
const messageType = ref('')

const formatDate = (dateString) => {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

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
    
    // Update auth store
    if (response.data.user) {
      authStore.updateUser(response.data.user)
    }
    
    // Reset form
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

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  // Initialize form with current user data
  if (authStore.user) {
    updateForm.value.name = authStore.user.name || ''
    updateForm.value.phone = authStore.user.phone || ''
    updateForm.value.address = authStore.user.address || ''
  }
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

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
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

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.action-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
}

.action-card:hover {
  background: #e9ecef;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.action-icon {
  font-size: 2.5rem;
}

.action-text h3 {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 0.25rem;
}

.action-text p {
  color: #666;
  font-size: 0.9rem;
}

.logout-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.logout-btn:hover {
  background: #c82333;
}

/* Update Form Styles */
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

/* Message Styles */
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

/* Responsive Adjustments */
@media (max-width: 768px) {
  .update-form {
    gap: 1rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .update-btn {
    width: 100%;
  }
}
</style>