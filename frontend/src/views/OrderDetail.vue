<template>
  <div class="order-detail">
    <div class="container">
      <h1 class="page-title">订单详情</h1>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="!order" class="empty-state">
        <div class="empty-state-icon">📋</div>
        <p class="empty-state-text">订单不存在</p>
        <router-link to="/orders" class="btn btn-primary">查看订单</router-link>
      </div>
      
      <div v-else class="order-content">
        <!-- 订单状态 -->
        <div class="order-status-card card">
          <div class="order-status-header">
            <h2 class="section-title">订单状态</h2>
            <span :class="['order-status', `status-${order.status}`]">
              {{ getStatusText(order.status) }}
            </span>
          </div>
          
          <div class="order-status-steps">
            <div 
              v-for="(step, index) in statusSteps" 
              :key="step.status"
              class="status-step"
              :class="{
                completed: index < currentStepIndex,
                active: index === currentStepIndex,
                pending: index > currentStepIndex
              }"
            >
              <div class="step-icon">{{ step.icon }}</div>
              <div class="step-content">
                <div class="step-title">{{ step.title }}</div>
                <div class="step-description">{{ step.description }}</div>
              </div>
              <div v-if="index < statusSteps.length - 1" class="step-line"></div>
            </div>
          </div>
        </div>
        
        <!-- 订单信息 -->
        <div class="order-info-card card">
          <h2 class="section-title">订单信息</h2>
          <div class="order-info-grid">
            <div class="info-item">
              <label>订单号</label>
              <span>{{ order.orderNumber || order.id }}</span>
            </div>
            <div class="info-item">
              <label>创建时间</label>
              <span>{{ formatDate(order.created_at) }}</span>
            </div>
            <div class="info-item">
              <label>支付方式</label>
              <span>{{ order.paymentMethod || '未选择' }}</span>
            </div>
            <div class="info-item">
              <label>订单总计</label>
              <span class="total-price">¥{{ order.totalPrice.toFixed(2) }}</span>
            </div>
          </div>
        </div>
        
        <!-- 收货信息 -->
        <div class="shipping-info-card card">
          <h2 class="section-title">收货信息</h2>
          <div class="shipping-info">
            <div class="info-item">
              <label>收货地址</label>
              <span>{{ order.shippingAddress.address }}</span>
            </div>
            <div class="info-item">
              <label>城市</label>
              <span>{{ order.shippingAddress.city }}</span>
            </div>
            <div class="info-item">
              <label>邮编</label>
              <span>{{ order.shippingAddress.postalCode }}</span>
            </div>
            <div class="info-item">
              <label>国家</label>
              <span>{{ order.shippingAddress.country }}</span>
            </div>
            <div class="info-item">
              <label>手机号码</label>
              <span>{{ order.shippingAddress.phone }}</span>
            </div>
          </div>
        </div>
        
        <!-- 商品信息 -->
        <div class="order-items-card card">
          <h2 class="section-title">订单商品</h2>
          <div 
            v-for="item in order.orderItems" 
            :key="item.product_id"
            class="order-item"
          >
            <img 
              :src="item.image || 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIiBmaWxsPSIjZjBmMGMwIi8+CjxwYXRoIGQ9Ik01MCA1MCBDNzcuNjEgNTAgMTAwIDIyLjYxIDEwMCAwIEMxMDAgMCA3Ny42MSAwIDUwIDAgQzIyLjM5IDAgMCAyMi42MSAwIDUwIEMwIDc3LjYxIDIyLjM5IDEwMCA1MCAxMDAiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEwIiBmaWxsPSIjMDAwIj5ObyBJbWFnZTwvdGV4dD4KPC9zdmc+'" 
              :alt="item.name" 
              class="item-image"
            />
            <div class="item-details">
              <h3 class="item-name">{{ item.name }}</h3>
              <p class="item-price">¥{{ item.price.toFixed(2) }} × {{ item.quantity }}</p>
            </div>
            <span class="item-total">¥{{ (item.price * item.quantity).toFixed(2) }}</span>
          </div>
        </div>
        
        <!-- 订单操作 -->
        <div class="order-actions-card card">
          <h2 class="section-title">订单操作</h2>
          <div class="order-actions">
            <button 
              v-if="order.status === 'pending'"
              class="btn btn-primary btn-lg"
              @click="handlePay"
              :disabled="processing"
            >
              {{ processing ? '处理中...' : '立即支付' }}
            </button>
            <button 
              v-if="order.status === 'pending'"
              class="btn btn-secondary btn-lg"
              @click="handleCancel"
              :disabled="processing"
            >
              {{ processing ? '处理中...' : '取消订单' }}
            </button>
            <button 
              v-if="order.status === 'shipped'"
              class="btn btn-primary btn-lg"
              @click="handleComplete"
              :disabled="processing"
            >
              {{ processing ? '处理中...' : '确认收货' }}
            </button>
            <router-link to="/orders" class="btn btn-outline-secondary btn-lg">
              返回订单列表
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/utils/api'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const processing = ref(false)
const order = ref(null)

const statusSteps = [
  {
    status: 'pending',
    title: '待付款',
    description: '请尽快完成支付',
    icon: '💳'
  },
  {
    status: 'processing',
    title: '待发货',
    description: '卖家正在准备发货',
    icon: '📦'
  },
  {
    status: 'shipped',
    title: '待收货',
    description: '商品正在配送中',
    icon: '🚚'
  },
  {
    status: 'delivered',
    title: '已完成',
    description: '订单已完成',
    icon: '✅'
  }
]

const statusOrder = {
  pending: 0,
  processing: 1,
  shipped: 2,
  delivered: 3,
  cancelled: 4
}

const currentStepIndex = computed(() => {
  if (!order.value) return 0
  return statusOrder[order.value.status] || 0
})

const getStatusText = (status) => {
  const statusMap = {
    pending: '待付款',
    processing: '待发货',
    shipped: '待收货',
    delivered: '已完成',
    cancelled: '已取消'
  }
  return statusMap[status] || status
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const fetchOrder = async () => {
  try {
    const response = await api.get(`/orders/${route.params.id}`)
    order.value = response.data
  } catch (error) {
    console.error('Failed to fetch order:', error)
    alert('获取订单失败，请重试')
  } finally {
    loading.value = false
  }
}

const handlePay = async () => {
  if (confirm('确认要支付此订单吗？')) {
    processing.value = true
    try {
      await api.put(`/orders/${order.value.id}/pay`)
      alert('支付成功！')
      await fetchOrder()
    } catch (error) {
      console.error('Failed to pay order:', error)
      alert('支付失败，请重试')
    } finally {
      processing.value = false
    }
  }
}

const handleCancel = async () => {
  if (confirm('确认要取消此订单吗？')) {
    processing.value = true
    try {
      await api.put(`/orders/${order.value.id}/cancel`)
      alert('订单取消成功！')
      await fetchOrder()
    } catch (error) {
      console.error('Failed to cancel order:', error)
      alert('取消订单失败，请重试')
    } finally {
      processing.value = false
    }
  }
}

const handleComplete = async () => {
  if (confirm('确认已收到商品吗？')) {
    processing.value = true
    try {
      await api.put(`/orders/${order.value.id}/complete`)
      alert('确认收货成功！')
      await fetchOrder()
    } catch (error) {
      console.error('Failed to complete order:', error)
      alert('确认收货失败，请重试')
    } finally {
      processing.value = false
    }
  }
}

onMounted(() => {
  fetchOrder()
})
</script>

<style scoped>
.order-detail {
  padding: 40px 0;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 32px;
  color: var(--text-primary);
}

.order-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.order-status-card,
.order-info-card,
.shipping-info-card,
.order-items-card,
.order-actions-card {
  padding: 24px;
}

/* 订单状态 */
.order-status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.order-status {
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 16px;
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

.order-status-steps {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.status-step {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  position: relative;
}

.status-step.completed .step-icon {
  background: #48bb78;
  color: white;
}

.status-step.active .step-icon {
  background: #3182ce;
  color: white;
}

.status-step.pending .step-icon {
  background: #e2e8f0;
  color: #718096;
}

.step-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.step-description {
  font-size: 14px;
  color: var(--text-secondary);
}

.step-line {
  position: absolute;
  left: 23px;
  top: 48px;
  bottom: -24px;
  width: 2px;
  background: #e2e8f0;
}

.status-step:last-child .step-line {
  display: none;
}

/* 订单信息 */
.order-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item label {
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 600;
}

.info-item span {
  font-size: 16px;
  color: var(--text-primary);
}

.total-price {
  font-weight: 700;
  color: var(--primary-color);
  font-size: 18px;
}

/* 收货信息 */
.shipping-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 订单商品 */
.order-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid var(--border-color);
}

.order-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 80px;
  height: 80px;
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

/* 订单操作 */
.order-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .order-status-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .order-info-grid {
    grid-template-columns: 1fr;
  }
  
  .order-actions {
    flex-direction: column;
  }
  
  .order-actions .btn {
    width: 100%;
  }
}
</style>