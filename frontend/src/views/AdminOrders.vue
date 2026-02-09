<template>
  <div class="admin-orders">
    <div class="container">
      <div class="page-header">
        <h1>订单管理</h1>
        <router-link to="/admin" class="btn btn-secondary">返回后台首页</router-link>
      </div>
      
      <div class="orders-list">
        <div class="search-bar">
          <input 
            v-model="searchQuery" 
            @input="handleSearch" 
            placeholder="按订单号/用户名搜索订单..."
            class="search-input"
          />
        </div>
        
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
        
        <div v-else-if="filteredOrders.length === 0" class="empty-state">
          <div class="empty-icon">📋</div>
          <p>暂无订单</p>
        </div>
        
        <div v-else class="orders-table-container">
          <table class="orders-table">
            <thead>
              <tr>
                <th>订单号</th>
                <th>用户ID</th>
                <th>总金额</th>
                <th>状态</th>
                <th>创建时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in filteredOrders" :key="order.id">
                <td>{{ order.orderNumber || order.id }}</td>
                <td>{{ order.user_id }}</td>
                <td>¥{{ order.totalPrice.toFixed(2) }}</td>
                <td>
                  <span :class="['order-status-badge', `status-${order.status}`]">
                    {{ getStatusText(order.status) }}
                  </span>
                </td>
                <td>{{ formatDate(order.created_at) }}</td>
                <td>
                  <button @click="viewOrderDetails(order.id)" class="btn btn-primary btn-sm">
                    查看详情
                  </button>
                  <button 
                    v-if="order.status === 'processing'"
                    @click="handleDeliver(order.id)"
                    class="btn btn-secondary btn-sm"
                  >
                    确认发货
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/utils/api'

const authStore = useAuthStore()
const router = useRouter()
const orders = ref([])
const filteredOrders = ref([])
const searchQuery = ref('')
const loading = ref(true)

onMounted(async () => {
  // Check if user is admin
  if (!authStore.user || authStore.user.role !== 'admin') {
    alert('您没有权限访问此页面')
    router.push('/')
    return
  }
  
  await fetchOrders()
})

const fetchOrders = async () => {
  try {
    const response = await api.get('/orders/all')
    orders.value = response.data
    
    // Initialize filtered orders
    filteredOrders.value = [...orders.value]
  } catch (error) {
    console.error('Failed to fetch orders:', error)
    alert('获取订单失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  if (!searchQuery.value) {
    filteredOrders.value = [...orders.value]
    return
  }
  
  const query = searchQuery.value.toLowerCase()
  filteredOrders.value = orders.value.filter(order => {
    return (order.orderNumber || order.id).toLowerCase().includes(query) || 
           order.user_id.toLowerCase().includes(query)
  })
}

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

const viewOrderDetails = (orderId) => {
  // 跳转到订单详情页面
  router.push(`/order/${orderId}`)
}

const handleDeliver = async (orderId) => {
  if (confirm('确认要发货此订单吗？')) {
    try {
      await api.put(`/orders/${orderId}/deliver`)
      alert('发货成功！')
      // 更新订单状态
      orderStatuses[orderId] = 'shipped'
      // 刷新订单列表
      await fetchOrders()
    } catch (error) {
      console.error('Failed to deliver order:', error)
      alert('发货失败，请重试')
    }
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}
</script>

<style scoped>
.admin-orders {
  padding: 40px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  color: var(--text-primary);
}

.orders-list {
  margin-top: 2rem;
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
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.orders-table-container {
  overflow-x: auto;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--bg-secondary);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.orders-table th,
.orders-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.orders-table th {
  background: var(--bg-primary);
  font-weight: 600;
  color: var(--text-primary);
}

.orders-table tr:hover {
  background: rgba(0, 0, 0, 0.02);
}

.order-status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  display: inline-block;
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

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .orders-table {
    font-size: 0.9rem;
  }
  
  .orders-table th,
  .orders-table td {
    padding: 0.75rem;
  }
}
</style>
