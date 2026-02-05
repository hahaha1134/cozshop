<template>
  <div class="admin-announcements">
    <div class="container">
      <div class="page-header">
        <h1>公告管理</h1>
        <router-link to="/admin" class="btn btn-secondary">返回后台首页</router-link>
      </div>
      
      <!-- Create Announcement Form -->
      <div class="create-announcement-section">
        <h2>发布新公告</h2>
        <form @submit.prevent="createAnnouncement" class="announcement-form">
          <div class="form-group">
            <label for="title">公告标题</label>
            <input 
              type="text" 
              id="title" 
              v-model="newAnnouncement.title" 
              required 
              class="form-control"
              placeholder="请输入公告标题"
            />
          </div>
          <div class="form-group">
            <label for="content">公告内容</label>
            <textarea 
              id="content" 
              v-model="newAnnouncement.content" 
              required 
              class="form-control"
              rows="5"
              placeholder="请输入公告内容"
            ></textarea>
          </div>
          <button type="submit" class="btn btn-primary" :disabled="submitting">
            {{ submitting ? '发布中...' : '发布公告' }}
          </button>
        </form>
      </div>
      
      <!-- Announcements List -->
      <div class="announcements-list-section">
        <h2>公告列表</h2>
        
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
        
        <div v-else-if="announcements.length === 0" class="empty-state">
          <div class="empty-icon">📢</div>
          <p>暂无公告</p>
        </div>
        
        <div v-else class="announcements-list">
          <div v-for="announcement in announcements" :key="announcement.id" class="announcement-item">
            <div class="announcement-header">
              <h3>{{ announcement.title }}</h3>
              <div class="announcement-actions">
                <button @click="editAnnouncement(announcement)" class="btn btn-sm btn-primary">
                  编辑
                </button>
                <button @click="deleteAnnouncement(announcement.id)" class="btn btn-sm btn-danger">
                  删除
                </button>
              </div>
            </div>
            <div class="announcement-content">
              {{ announcement.content }}
            </div>
            <div class="announcement-meta">
              {{ formatDate(announcement.created_at) }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- Edit Modal -->
      <div v-if="editingAnnouncement" class="modal-overlay" @click="closeEditModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>编辑公告</h2>
            <button @click="closeEditModal" class="modal-close">&times;</button>
          </div>
          <form @submit.prevent="updateAnnouncement" class="announcement-form">
            <div class="form-group">
              <label for="edit-title">公告标题</label>
              <input 
                type="text" 
                id="edit-title" 
                v-model="editingAnnouncement.title" 
                required 
                class="form-control"
              />
            </div>
            <div class="form-group">
              <label for="edit-content">公告内容</label>
              <textarea 
                id="edit-content" 
                v-model="editingAnnouncement.content" 
                required 
                class="form-control"
                rows="5"
              ></textarea>
            </div>
            <div class="modal-actions">
              <button type="button" @click="closeEditModal" class="btn btn-secondary">
                取消
              </button>
              <button type="submit" class="btn btn-primary" :disabled="updating">
                {{ updating ? '更新中...' : '更新公告' }}
              </button>
            </div>
          </form>
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

// State
const announcements = ref([])
const loading = ref(true)
const submitting = ref(false)
const updating = ref(false)
const newAnnouncement = ref({
  title: '',
  content: ''
})
const editingAnnouncement = ref(null)

onMounted(async () => {
  // Check if user is admin
  if (!authStore.user || authStore.user.role !== 'admin') {
    alert('您没有权限访问此页面')
    router.push('/')
    return
  }
  
  await fetchAnnouncements()
})

// Fetch all announcements
const fetchAnnouncements = async () => {
  try {
    loading.value = true
    const response = await api.get('/system/announcements')
    announcements.value = response.data
  } catch (error) {
    console.error('Failed to fetch announcements:', error)
    alert('获取公告列表失败')
  } finally {
    loading.value = false
  }
}

// Create new announcement
const createAnnouncement = async () => {
  try {
    submitting.value = true
    await api.post('/system/announcements', {
      title: newAnnouncement.value.title,
      content: newAnnouncement.value.content
    })
    alert('公告发布成功')
    
    // Reset form
    newAnnouncement.value = {
      title: '',
      content: ''
    }
    
    // Refresh list
    await fetchAnnouncements()
  } catch (error) {
    console.error('Failed to create announcement:', error)
    alert('发布公告失败')
  } finally {
    submitting.value = false
  }
}

// Edit announcement
const editAnnouncement = (announcement) => {
  editingAnnouncement.value = { ...announcement }
}

// Close edit modal
const closeEditModal = () => {
  editingAnnouncement.value = null
}

// Update announcement
const updateAnnouncement = async () => {
  if (!editingAnnouncement.value) return
  
  try {
    updating.value = true
    await api.put(`/system/announcements/${editingAnnouncement.value.id}`, {
      title: editingAnnouncement.value.title,
      content: editingAnnouncement.value.content
    })
    alert('公告更新成功')
    closeEditModal()
    await fetchAnnouncements()
  } catch (error) {
    console.error('Failed to update announcement:', error)
    alert('更新公告失败')
  } finally {
    updating.value = false
  }
}

// Delete announcement
const deleteAnnouncement = async (announcementId) => {
  if (!confirm('确定要删除此公告吗？')) return
  
  try {
    await api.delete(`/system/announcements/${announcementId}`)
    alert('公告删除成功')
    await fetchAnnouncements()
  } catch (error) {
    console.error('Failed to delete announcement:', error)
    alert('删除公告失败')
  }
}

// Format date
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}
</script>

<style scoped>
.admin-announcements {
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

/* Create Announcement Section */
.create-announcement-section {
  margin-bottom: 3rem;
  background: var(--bg-secondary);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
}

.create-announcement-section h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
}

.announcement-form {
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
  color: var(--text-secondary);
}

.form-control {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-control textarea {
  resize: vertical;
  min-height: 120px;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
  transform: translateY(-2px);
}

.btn-primary:disabled {
  background: #6c757d;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

/* Announcements List Section */
.announcements-list-section {
  margin-top: 3rem;
}

.announcements-list-section h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  background: var(--bg-secondary);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-state p {
  font-size: 1.1rem;
  color: var(--text-secondary);
}

.announcements-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.announcement-item {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.3s, box-shadow 0.3s;
}

.announcement-item:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.announcement-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.announcement-header h3 {
  font-size: 1.3rem;
  color: var(--text-primary);
  margin: 0;
  flex: 1;
}

.announcement-actions {
  display: flex;
  gap: 0.75rem;
}

.announcement-content {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--text-secondary);
  margin-bottom: 1rem;
  white-space: pre-wrap;
}

.announcement-meta {
  font-size: 0.9rem;
  color: var(--text-muted);
  border-top: 1px solid var(--border-color);
  padding-top: 1rem;
  text-align: right;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: var(--shadow-lg);
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-header h2 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-muted);
  transition: color 0.3s;
}

.modal-close:hover {
  color: var(--text-primary);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .create-announcement-section {
    padding: 1.5rem;
  }
  
  .announcement-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .announcement-actions {
    align-self: flex-end;
  }
  
  .modal-content {
    padding: 1.5rem;
  }
}
</style>