<template>
  <div class="admin-panel">
    <div class="container">
      <h1>管理后台</h1>
      
      <!-- Dashboard Section -->
      <div class="dashboard-section">
        <h2>数据概览</h2>
        
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
        
        <div v-else class="dashboard-content">
          <!-- Stats Cards -->
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">📦</div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.total_products }}</div>
                <div class="stat-label">商品总数</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">📋</div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.total_orders }}</div>
                <div class="stat-label">订单总数</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">👥</div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.total_users }}</div>
                <div class="stat-label">用户总数</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">💰</div>
              <div class="stat-info">
                <div class="stat-value">¥{{ stats.total_revenue }}</div>
                <div class="stat-label">总收入</div>
              </div>
            </div>
          </div>
          
          <!-- Today's New Data -->
          <div class="today-section">
            <h3>今日新增</h3>
            <div class="today-grid">
              <div class="today-card">
                <div class="today-icon">✨</div>
                <div class="today-info">
                  <div class="today-value">{{ todayStats.products }}</div>
                  <div class="today-label">新增商品</div>
                </div>
              </div>
              <div class="today-card">
                <div class="today-icon">📈</div>
                <div class="today-info">
                  <div class="today-value">{{ todayStats.orders }}</div>
                  <div class="today-label">新增订单</div>
                </div>
              </div>
              <div class="today-card">
                <div class="today-icon">👤</div>
                <div class="today-info">
                  <div class="today-value">{{ todayStats.users }}</div>
                  <div class="today-label">新增用户</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Charts Section -->
          <div class="charts-section">
            <h3>数据可视化</h3>
            <div class="charts-grid">
              <div class="chart-card">
                <h4>月度销售趋势</h4>
                <div ref="salesChartRef" class="chart-container"></div>
              </div>
              <div class="chart-card">
                <h4>订单状态分布</h4>
                <div ref="orderStatusChartRef" class="chart-container"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Menu Section -->
      <div class="admin-menu">
        <h2>管理功能</h2>
        <div class="menu-grid">
          <div class="menu-item">
            <router-link to="/admin/products" class="menu-link">
              <div class="menu-icon">📦</div>
              <div class="menu-text">商品管理</div>
            </router-link>
          </div>
          <div class="menu-item">
            <router-link to="/admin/orders" class="menu-link">
              <div class="menu-icon">📋</div>
              <div class="menu-text">订单管理</div>
            </router-link>
          </div>
          <div class="menu-item">
            <router-link to="/admin/users" class="menu-link">
              <div class="menu-icon">👥</div>
              <div class="menu-text">用户管理</div>
            </router-link>
          </div>
          <div class="menu-item">
            <router-link to="/admin/system" class="menu-link">
              <div class="menu-icon">⚙️</div>
              <div class="menu-text">系统管理</div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/utils/api'
import * as echarts from 'echarts'

const authStore = useAuthStore()
const router = useRouter()

// Refs for charts
const salesChartRef = ref(null)
const orderStatusChartRef = ref(null)

// Chart instances
let salesChart = null
let orderStatusChart = null

// State
const loading = ref(true)
const stats = ref({
  total_products: 0,
  total_orders: 0,
  total_users: 0,
  total_revenue: 0
})
const todayStats = ref({
  products: 0,
  orders: 0,
  users: 0
})
const salesData = ref([])
const orderStatuses = ref({})

// Fetch data from API
const fetchData = async () => {
  try {
    // Fetch system status
    const statusResponse = await api.get('/system/status')
    const statusData = statusResponse.data
    stats.value = {
      total_products: statusData.statistics.total_products,
      total_orders: statusData.statistics.total_orders,
      total_users: statusData.statistics.total_users,
      total_revenue: statusData.statistics.total_revenue
    }
    orderStatuses.value = statusData.statistics.order_statuses
    
    // Fetch today's stats
    const todayResponse = await api.get('/system/today')
    todayStats.value = todayResponse.data.today
    
    // Fetch sales data
    const statsResponse = await api.get('/system/stats')
    salesData.value = statsResponse.data.monthly_sales
    
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
    alert('获取数据失败，请重试')
  } finally {
    loading.value = false
    // Initialize charts after data is loaded
    if (!loading.value) {
      initCharts()
    }
  }
}

// Initialize ECharts
const initCharts = () => {
  // Sales chart
  if (salesChartRef.value) {
    salesChart = echarts.init(salesChartRef.value)
    const salesOption = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
          label: {
            backgroundColor: '#6a7985'
          }
        }
      },
      legend: {
        data: ['订单数', '销售额']
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: salesData.value.map(item => item.month)
      },
      yAxis: [
        {
          type: 'value',
          name: '订单数',
          position: 'left'
        },
        {
          type: 'value',
          name: '销售额',
          position: 'right',
          axisLabel: {
            formatter: '¥{value}'
          }
        }
      ],
      series: [
        {
          name: '订单数',
          type: 'line',
          data: salesData.value.map(item => item.orders),
          smooth: true,
          itemStyle: {
            color: '#5470c6'
          }
        },
        {
          name: '销售额',
          type: 'bar',
          yAxisIndex: 1,
          data: salesData.value.map(item => item.revenue),
          itemStyle: {
            color: '#91cc75'
          }
        }
      ]
    }
    salesChart.setOption(salesOption)
  }
  
  // Order status chart
  if (orderStatusChartRef.value) {
    orderStatusChart = echarts.init(orderStatusChartRef.value)
    const orderStatusOption = {
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: '订单状态',
          type: 'pie',
          radius: '50%',
          data: [
            { value: orderStatuses.value.pending, name: '待处理' },
            { value: orderStatuses.value.processing, name: '处理中' },
            { value: orderStatuses.value.shipped, name: '已发货' },
            { value: orderStatuses.value.delivered, name: '已送达' },
            { value: orderStatuses.value.cancelled, name: '已取消' }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    }
    orderStatusChart.setOption(orderStatusOption)
  }
}

// Handle window resize
const handleResize = () => {
  if (salesChart) salesChart.resize()
  if (orderStatusChart) orderStatusChart.resize()
}

onMounted(async () => {
  // Check if user is admin
  if (!authStore.user || authStore.user.role !== 'admin') {
    alert('您没有权限访问管理后台')
    router.push('/')
    return
  }
  
  // Fetch dashboard data
  await fetchData()
  
  // Add resize listener
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  // Clean up
  if (salesChart) salesChart.dispose()
  if (orderStatusChart) orderStatusChart.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.admin-panel {
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

h2 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--border-color);
}

h3 {
  font-size: 1.4rem;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

h4 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: var(--text-secondary);
}

/* Dashboard Section */
.dashboard-section {
  margin-bottom: 3rem;
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

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: var(--shadow-sm);
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
}

.stat-label {
  font-size: 1rem;
  color: var(--text-secondary);
}

/* Today Section */
.today-section {
  margin-bottom: 2rem;
}

.today-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.today-card {
  background: var(--bg-secondary);
  border-radius: 10px;
  padding: 1.2rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  box-shadow: var(--shadow-sm);
}

.today-icon {
  font-size: 2rem;
}

.today-info {
  flex: 1;
}

.today-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

.today-label {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

/* Charts Section */
.charts-section {
  margin-bottom: 3rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.chart-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
}

.chart-container {
  width: 100%;
  height: 300px;
}

/* Menu Section */
.admin-menu {
  margin-top: 3rem;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.menu-item {
  background: var(--bg-secondary);
  border-radius: 12px;
  box-shadow: var(--shadow-md);
  transition: transform 0.3s, box-shadow 0.3s;
}

.menu-item:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
}

.menu-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2.5rem 2rem;
  text-decoration: none;
  color: var(--text-primary);
}

.menu-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.menu-text {
  font-size: 1.1rem;
  font-weight: 600;
}

/* Responsive Design */
@media (max-width: 768px) {
  h1 {
    font-size: 2rem;
  }
  
  h2 {
    font-size: 1.5rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .today-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 250px;
  }
  
  .menu-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .today-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
  }
  
  .today-card {
    flex-direction: column;
    text-align: center;
  }
}
</style>