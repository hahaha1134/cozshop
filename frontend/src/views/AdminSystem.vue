<template>
  <div class="admin-system">
    <div class="container">
      <div class="page-header">
        <h1>系统管理</h1>
        <router-link to="/admin" class="btn btn-secondary">返回后台首页</router-link>
      </div>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>
      
      <div v-else class="system-content">
        <!-- System Status -->
        <div class="status-card">
          <h2>系统状态</h2>
          <div class="status-info">
            <div class="status-item">
              <span class="status-label">状态:</span>
              <span class="status-value" :class="{ 'status-operational': systemStatus.status === 'operational' }">
                {{ systemStatus.status === 'operational' ? '运行正常' : '异常' }}
              </span>
            </div>
            <div class="status-item">
              <span class="status-label">时间:</span>
              <span class="status-value">{{ formatDate(systemStatus.timestamp) }}</span>
            </div>
          </div>
        </div>
        
        <!-- System Statistics -->
        <div class="stats-card">
          <h2>系统统计</h2>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-icon">👥</div>
              <div class="stat-info">
                <div class="stat-value">{{ systemStats.statistics?.total_users || 0 }}</div>
                <div class="stat-label">总用户数</div>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">📦</div>
              <div class="stat-info">
                <div class="stat-value">{{ systemStats.statistics?.total_products || 0 }}</div>
                <div class="stat-label">总商品数</div>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">📋</div>
              <div class="stat-info">
                <div class="stat-value">{{ systemStats.statistics?.total_orders || 0 }}</div>
                <div class="stat-label">总订单数</div>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">💰</div>
              <div class="stat-info">
                <div class="stat-value">¥{{ systemStats.statistics?.total_revenue || 0 }}</div>
                <div class="stat-label">总收入</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- System Announcements -->
        <div class="announcements-card">
          <h2>系统公告管理</h2>
          <div class="announcement-actions">
            <button @click="showAnnouncementForm = true" class="btn btn-primary">发布新公告</button>
          </div>
          <div v-if="announcements.length === 0" class="empty-announcements">
            <p>暂无系统公告</p>
          </div>
          <div v-else class="announcements-list">
            <div v-for="announcement in announcements" :key="announcement.id" class="announcement-item">
              <div class="announcement-content">
                <h3>{{ announcement.title }}</h3>
                <p>{{ announcement.content }}</p>
                <span class="announcement-date">{{ formatDate(announcement.created_at) }}</span>
              </div>
              <div class="announcement-actions">
                <button @click="editAnnouncement(announcement)" class="btn btn-primary btn-sm">编辑</button>
                <button @click="deleteAnnouncement(announcement.id)" class="btn btn-danger btn-sm">删除</button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Data Management -->
        <div class="data-card">
          <h2>数据管理</h2>
          <div class="data-actions">
            <button @click="cleanupInvalidData" class="btn btn-danger" :disabled="cleaningData">
              {{ cleaningData ? '清理中...' : '清理无效数据' }}
            </button>
          </div>
          <p class="data-info">清理平台无效数据，包括未完成的订单、无效的用户账号等。</p>
        </div>
        
        <!-- Announcement Form Modal -->
        <div v-if="showAnnouncementForm" class="modal-overlay" @click="showAnnouncementForm = false">
          <div class="modal-content" @click.stop>
            <h3>{{ editingAnnouncement ? '编辑公告' : '发布新公告' }}</h3>
            <form @submit.prevent="saveAnnouncement">
              <div class="form-group">
                <label for="announcement-title">标题</label>
                <input 
                  id="announcement-title" 
                  v-model="announcementForm.title" 
                  required 
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="announcement-content">内容</label>
                <textarea 
                  id="announcement-content" 
                  v-model="announcementForm.content" 
                  required 
                  rows="4"
                  class="form-textarea"
                ></textarea>
              </div>
              <div class="form-actions">
                <button type="button" @click="showAnnouncementForm = false" class="btn btn-secondary">取消</button>
                <button type="submit" class="btn btn-primary" :disabled="savingAnnouncement">
                  {{ savingAnnouncement ? '保存中...' : '保存' }}
                </button>
              </div>
            </form>
          </div>
        </div>
        
        <!-- Order Status -->
        <div class="order-status-card">
          <h2>订单状态</h2>
          <div class="status-grid">
            <div class="status-item">
              <div class="status-label">待处理</div>
              <div class="status-value">{{ systemStats.statistics.order_statuses.pending }}</div>
            </div>
            <div class="status-item">
              <div class="status-label">处理中</div>
              <div class="status-value">{{ systemStats.statistics.order_statuses.processing }}</div>
            </div>
            <div class="status-item">
              <div class="status-label">已发货</div>
              <div class="status-value">{{ systemStats.statistics.order_statuses.shipped }}</div>
            </div>
            <div class="status-item">
              <div class="status-label">已送达</div>
              <div class="status-value">{{ systemStats.statistics.order_statuses.delivered }}</div>
            </div>
            <div class="status-item">
              <div class="status-label">已取消</div>
              <div class="status-value">{{ systemStats.statistics.order_statuses.cancelled }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/utils/api'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const systemStatus = ref({})
const systemStats = ref({})
const announcements = ref([])
const showAnnouncementForm = ref(false)
const announcementForm = ref({ title: '', content: '' })
const editingAnnouncement = ref(null)
const savingAnnouncement = ref(false)
const cleaningData = ref(false)

onMounted(async () => {
  // Check if user is admin
  if (!authStore.user || authStore.user.role !== 'admin') {
    alert('您没有权限访问管理后台')
    router.push('/')
    return
  }
  
  await fetchSystemStatus()
  await fetchSystemStats()
  await fetchAnnouncements()
})

const fetchSystemStatus = async () => {
  try {
    const response = await api.get('/system/status')
    systemStatus.value = response.data
  } catch (error) {
    console.error('Failed to fetch system status:', error)
    alert('获取系统状态失败')
  }
}

const fetchSystemStats = async () => {
  try {
    const response = await api.get('/system/status')
    systemStats.value = response.data
  } catch (error) {
    console.error('Failed to fetch system statistics:', error)
    alert('获取系统统计数据失败')
  }
}

const fetchAnnouncements = async () => {
  try {
    const response = await api.get('/system/announcements')
    announcements.value = response.data
  } catch (error) {
    console.error('Failed to fetch announcements:', error)
    // 静默失败，因为这可能是新功能
  }
}

const saveAnnouncement = async () => {
  savingAnnouncement.value = true
  try {
    if (editingAnnouncement.value) {
      // Edit existing announcement
      await api.put(`/system/announcements/${editingAnnouncement.value.id}`, announcementForm.value)
      alert('公告更新成功')
    } else {
      // Create new announcement
      await api.post('/system/announcements', announcementForm.value)
      alert('公告发布成功')
    }
    await fetchAnnouncements()
    showAnnouncementForm.value = false
    resetAnnouncementForm()
  } catch (error) {
    console.error('Failed to save announcement:', error)
    alert('保存公告失败')
  } finally {
    savingAnnouncement.value = false
  }
}

const editAnnouncement = (announcement) => {
  editingAnnouncement.value = announcement
  announcementForm.value = { ...announcement }
  showAnnouncementForm.value = true
}

const deleteAnnouncement = async (announcementId) => {
  if (confirm('确定要删除此公告吗？')) {
    try {
      await api.delete(`/system/announcements/${announcementId}`)
      alert('公告删除成功')
      await fetchAnnouncements()
    } catch (error) {
      console.error('Failed to delete announcement:', error)
      alert('删除公告失败')
    }
  }
}

const resetAnnouncementForm = () => {
  announcementForm.value = { title: '', content: '' }
  editingAnnouncement.value = null
}

const cleanupInvalidData = async () => {
  if (confirm('确定要清理平台无效数据吗？此操作不可恢复。')) {
    cleaningData.value = true
    try {
      await api.post('/system/cleanup')
      alert('数据清理成功')
    } catch (error) {
      console.error('Failed to cleanup data:', error)
      alert('数据清理失败')
    } finally {
      cleaningData.value = false
    }
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}
</script>

<style scoped>
.admin-system {
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

.system-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.status-card,
.stats-card,
.order-status-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: var(--shadow-sm);
}

h2 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--border-color);
}

.status-info {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-label {
  font-weight: 600;
  color: var(--text-secondary);
}

.status-value {
  color: var(--text-primary);
}

.status-operational {
  color: #27ae60;
  font-weight: 600;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-item {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: var(--shadow-sm);
}

.stat-icon {
  font-size: 2rem;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

.stat-label {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.status-item {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: var(--shadow-sm);
}

.status-item .status-label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.status-item .status-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .status-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .status-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
