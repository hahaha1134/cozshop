<template>
  <div class="admin-orders">
    <div class="container">
      <div class="page-header">
        <h1>订单管理</h1>
        <router-link to="/admin" class="btn btn-secondary">返回后台首页</router-link>
      </div>
      
      <div class="orders-list">
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
        
        <div v-else-if="orders.length === 0" class="empty-state">
          <div class="empty-icon">📋</div>
          <p>暂无订单</p>
        </div>
        
        <div v-else class="orders-table-container">
          <table class="orders-table">
            <thead>
              <tr>
                <th>订单ID</th>
                <th>用户ID</th>
                <th>总金额</th>
                <th>状态</th>
                <th>创建时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id">
                <td>{{ order.id }}</td>
                <td>{{ order.user_id }}</td>
                <td>¥{{ order.totalPrice.toFixed(2) }}</td>
                <td>
                  <select v-model="orderStatuses[order.id]" @change="updateOrderStatus(order.id, orderStatuses[order.id])" class="status-select">
                    <option value="pending">待处理</option>
                    <option value="processing">处理中</option>
                    <option value="shipped">已发货</option>
                    <option value="delivered">已送达</option>
                    <option value="cancelled">已取消</option>
                  </select>
                </td>
                <td>{{ formatDate(order.created_at) }}</td>
                <td>
                  <button @click="viewOrderDetails(order.id)" class="btn btn-primary btn-sm">
                    查看详情
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
const loading = ref(true)
const orderStatuses = reactive({})

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
    
    // Initialize order statuses
    orders.value.forEach(order => {
      orderStatuses[order.id] = order.status
    })
  } catch (error) {
    console.error('Failed to fetch orders:', error)
    alert('获取订单失败')
  } finally {
    loading.value = false
  }
}

const updateOrderStatus = async (orderId, newStatus) => {
  try {
    await api.put(`/orders/${orderId}/status`, { status: newStatus })
    alert('订单状态更新成功')
  } catch (error) {
    console.error('Failed to update order status:', error)
    alert('更新订单状态失败')
    // Revert status if update fails
    const order = orders.value.find(o => o.id === orderId)
    if (order) {
      orderStatuses[orderId] = order.status
    }
  }
}

const viewOrderDetails = (orderId) => {
  // In a real app, you might navigate to an order details page
  alert(`查看订单 ${orderId} 的详细信息`)
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

.status-select {
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: white;
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
