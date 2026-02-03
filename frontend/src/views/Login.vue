<template>
  <div class="login">
    <div class="container">
      <div class="auth-container">
        <div class="auth-card card">
          <h1 class="auth-title">登录</h1>
          
          <form @submit.prevent="handleLogin" class="auth-form">
            <div class="form-group">
              <label for="email">邮箱</label>
              <input
                id="email"
                v-model="formData.email"
                type="email"
                required
                placeholder="请输入邮箱"
              />
            </div>
            
            <div class="form-group">
              <label for="password">密码</label>
              <input
                id="password"
                v-model="formData.password"
                type="password"
                required
                placeholder="请输入密码"
              />
            </div>
            
            <button 
              type="submit" 
              class="btn btn-primary btn-lg"
              :disabled="loading"
            >
              {{ loading ? '登录中...' : '登录' }}
            </button>
          </form>
          
          <p class="auth-footer">
            还没有账号？
            <router-link to="/register">立即注册</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  email: '',
  password: ''
})

const loading = ref(false)

const handleLogin = async () => {
  loading.value = true
  try {
    await authStore.login(formData.value)
    router.push('/')
  } catch (error) {
    console.error('Login failed:', error)
    alert('登录失败，请检查邮箱和密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  padding: 40px 0;
}

.auth-container {
  max-width: 400px;
  margin: 0 auto;
}

.auth-card {
  padding: 40px;
}

.auth-title {
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 32px;
  color: var(--text-primary);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: var(--text-primary);
}

.form-group input {
  padding: 12px 16px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.auth-footer {
  text-align: center;
  margin-top: 24px;
  color: var(--text-secondary);
}

.auth-footer a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
}

.auth-footer a:hover {
  text-decoration: underline;
}
</style>