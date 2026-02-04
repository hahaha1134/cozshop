<template>
  <div class="admin-users">
    <div class="container">
      <div class="page-header">
        <h1>用户管理</h1>
        <router-link to="/admin" class="btn btn-secondary">返回后台首页</router-link>
      </div>
      
      <div class="users-list">
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
        
        <div v-else-if="users.length === 0" class="empty-state">
          <div class="empty-icon">👥</div>
          <p>暂无用户</p>
        </div>
        
        <div v-else class="users-table-container">
          <table class="users-table">
            <thead>
              <tr>
                <th>用户ID</th>
                <th>姓名</th>
                <th>邮箱</th>
                <th>角色</th>
                <th>注册时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
                <td>
                  <select v-model="userRoles[user.id]" @change="updateUserRole(user.id, userRoles[user.id])" class="role-select">
                    <option value="user">用户</option>
                    <option value="admin">管理员</option>
                  </select>
                </td>
                <td>{{ formatDate(user.created_at) }}</td>
                <td>
                  <button @click="deleteUser(user.id)" class="btn btn-danger btn-sm">
                    删除
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

const router = useRouter()
const authStore = useAuthStore()

const users = ref([])
const loading = ref(true)
const userRoles = reactive({})

onMounted(async () => {
  // Check if user is admin
  if (!authStore.user || authStore.user.role !== 'admin') {
    alert('您没有权限访问管理后台')
    router.push('/')
    return
  }
  
  await fetchUsers()
})

const fetchUsers = async () => {
  try {
    const response = await api.get('/users')
    users.value = response.data
    
    // Initialize user roles
    users.value.forEach(user => {
      userRoles[user.id] = user.role
    })
  } catch (error) {
    console.error('Failed to fetch users:', error)
    alert('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const updateUserRole = async (userId, role) => {
  try {
    await api.put(`/users/${userId}/role`, { role })
    alert('用户角色更新成功')
  } catch (error) {
    console.error('Failed to update user role:', error)
    alert('更新用户角色失败')
    // Revert role if update fails
    const user = users.value.find(u => u.id === userId)
    if (user) {
      userRoles[userId] = user.role
    }
  }
}

const deleteUser = async (userId) => {
  if (confirm('确定要删除此用户吗？')) {
    try {
      await api.delete(`/users/${userId}`)
      alert('用户删除成功')
      await fetchUsers()
    } catch (error) {
      console.error('Failed to delete user:', error)
      alert('删除用户失败')
    }
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}
</script>

<style scoped>
.admin-users {
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

.users-list {
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

.users-table-container {
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--bg-secondary);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.users-table th,
.users-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.users-table th {
  background: var(--bg-primary);
  font-weight: 600;
  color: var(--text-primary);
}

.users-table tr:hover {
  background: rgba(0, 0, 0, 0.02);
}

.role-select {
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
  
  .users-table {
    font-size: 0.9rem;
  }
  
  .users-table th,
  .users-table td {
    padding: 0.75rem;
  }
}
</style>
