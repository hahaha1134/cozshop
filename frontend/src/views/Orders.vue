<template>
  <div class="orders">
    <div class="container">
      <h1 class="page-title">我的订单</h1>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="orders.length === 0" class="empty-state">
        <div class="empty-state-icon">📋</div>
        <p class="empty-state-text">暂无订单</p>
        <router-link to="/" class="btn btn-primary">去购物</router-link>
      </div>
      
      <div v-else class="orders-list">
        <div 
          v-for="order in orders" 
          :key="order.id"
          class="order-card card"
        >
          <div class="order-header">
            <div class="order-info">
              <span class="order-id">订单号: {{ order.orderNumber || order.id }}</span>
              <span class="order-date">{{ formatDate(order.created_at) }}</span>
            </div>
            <span :class="['order-status', `status-${order.status}`]">
              {{ getStatusText(order.status) }}
            </span>
          </div>
          
          <div class="order-items">
            <div 
              v-for="item in order.orderItems" 
              :key="item.product_id"
              class="order-item"
            >
              <img 
                :src="item.image || 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIiBmaWxsPSIjZjBmMGMwIi8+CjxwYXRoIGQ9Ik01MCA1MCBDNzcuNjEgNTAgMTAwIDIyLjYxIDEwMCAwIEMxMDAgMCA3Ny42MSAwIDUwIDAgQzIyLjM5IDAgMCAyMi42MSAwIDUwIEMwIDc3LjYxIDIyLjM5IDEwMCA1MCAxMDAiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEwIiBmaWxsPSIjMDAwIj5ObyBJbWFnZTwvdGV4dD4KPC9zdmc='" 
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
              <button 
                class="btn btn-secondary btn-sm"
                @click="viewOrderDetails(order.id)"
              >
                查看详情
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
import api from '@/utils/api'

const router = useRouter()

const orders = ref([])
const loading = ref(true)

const fetchOrders = async () => {
  try {
    const response = await api.get('/orders')
    orders.value = response.data
  } catch (error) {
    console.error('Failed to fetch orders:', error)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusText = (status) => {
  const statusMap = {
    pending: '待处理',
    processing: '处理中',
    shipped: '已发货',
    delivered: '已送达',
    cancelled: '已取消'
  }
  return statusMap[status] || status
}

const viewOrderDetails = (orderId) => {
  router.push(`/order/${orderId}`)
}

onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.orders {
  padding: 40px 0;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 32px;
  color: var(--text-primary);
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.order-card {
  padding: 24px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 16px;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.order-id {
  font-weight: 600;
  color: var(--text-primary);
}

.order-date {
  font-size: 14px;
  color: var(--text-secondary);
}

.order-status {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
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
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 16px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.item-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
}

.item-details {
  flex: 1;
}

.item-name {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 4px 0;
  color: var(--text-primary);
}

.item-price {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.item-total {
  font-weight: 600;
  color: var(--text-primary);
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
}

.order-total {
  font-size: 18px;
  font-weight: 700;
}

.order-total span:last-child {
  color: var(--primary-color);
  margin-left: 8px;
}

.order-actions {
  display: flex;
  gap: 8px;
}

@media (max-width: 768px) {
  .order-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .order-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
}
</style>