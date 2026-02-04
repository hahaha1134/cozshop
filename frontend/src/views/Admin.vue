<template>
  <div class="admin-panel">
    <div class="container">
      <h1>管理后台</h1>
      <div class="admin-menu">
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
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  // Check if user is admin
  if (!authStore.user || authStore.user.role !== 'admin') {
    alert('您没有权限访问管理后台')
    router.push('/')
  }
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

.admin-menu {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
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
  padding: 3rem 2rem;
  text-decoration: none;
  color: var(--text-primary);
}

.menu-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.menu-text {
  font-size: 1.2rem;
  font-weight: 600;
}

@media (max-width: 768px) {
  .admin-menu {
    grid-template-columns: 1fr;
  }
  
  h1 {
    font-size: 2rem;
  }
}
</style>
