<template>
  <header class="header">
    <div class="container">
      <div class="header-content">
        <router-link to="/" class="logo">
          CozShop
        </router-link>
        
        <nav class="nav">
          <router-link to="/" class="nav-link">首页</router-link>
          <router-link v-if="authStore.isAuthenticated" to="/orders" class="nav-link">我的订单</router-link>
          <router-link v-if="authStore.isAuthenticated" to="/profile" class="nav-link">个人中心</router-link>
        </nav>
        
        <div class="header-actions">
          <router-link v-if="authStore.isAuthenticated" to="/cart" class="cart-link">
            <span class="cart-icon">🛒</span>
            <span v-if="cartStore.totalItems > 0" class="cart-badge">
              {{ cartStore.totalItems }}
            </span>
          </router-link>
          
          <div v-if="authStore.isAuthenticated" class="user-menu">
            <span class="user-name">{{ authStore.user?.name }}</span>
            <button @click="handleLogout" class="btn btn-secondary btn-sm">退出</button>
          </div>
          <div v-else class="auth-buttons">
            <router-link to="/login" class="btn btn-secondary btn-sm">登录</router-link>
            <router-link to="/register" class="btn btn-primary btn-sm">注册</router-link>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'

const authStore = useAuthStore()
const cartStore = useCartStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

onMounted(async () => {
  if (authStore.isAuthenticated) {
    try {
      await cartStore.fetchCart()
    } catch (error) {
      console.error('Failed to fetch cart:', error)
    }
  }
})
</script>

<style scoped>
.header {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0;
}

.logo {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-decoration: none;
}

.nav {
  display: flex;
  gap: 24px;
}

.nav-link {
  color: var(--text-primary);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--primary-color);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.cart-link {
  position: relative;
  text-decoration: none;
  color: var(--text-primary);
  font-size: 20px;
}

.cart-icon {
  display: block;
}

.cart-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: var(--danger-color);
  color: white;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 16px;
  text-align: center;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-name {
  font-weight: 500;
  color: var(--text-primary);
}

.auth-buttons {
  display: flex;
  gap: 8px;
}

@media (max-width: 768px) {
  .header-content {
    flex-wrap: wrap;
    gap: 12px;
  }
  
  .nav {
    order: 3;
    width: 100%;
    justify-content: center;
    gap: 16px;
  }
}
</style>