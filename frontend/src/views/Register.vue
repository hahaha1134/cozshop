<template>
  <div class="register">
    <div class="container">
      <div class="auth-container">
        <div class="auth-card card">
          <h1 class="auth-title">注册</h1>
          
          <form @submit.prevent="handleRegister" class="auth-form">
            <div class="form-group">
              <label for="name">用户名</label>
              <input
                id="name"
                v-model="formData.name"
                type="text"
                required
                placeholder="请输入用户名"
              />
            </div>
            
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
                placeholder="请输入密码（至少6位）"
                minlength="6"
              />
            </div>
            
            <div class="form-group">
              <label for="confirmPassword">确认密码</label>
              <input
                id="confirmPassword"
                v-model="formData.confirmPassword"
                type="password"
                required
                placeholder="请再次输入密码"
              />
            </div>
            
            <button 
              type="submit" 
              class="btn btn-primary btn-lg"
              :disabled="loading"
            >
              {{ loading ? '注册中...' : '注册' }}
            </button>
          </form>
          
          <p class="auth-footer">
            已有账号？
            <router-link to="/login">立即登录</router-link>
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
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)

const handleRegister = async () => {
  if (formData.value.password !== formData.value.confirmPassword) {
    alert('两次输入的密码不一致')
    return
  }
  
  loading.value = true
  try {
    await authStore.register({
      name: formData.value.name,
      email: formData.value.email,
      password: formData.value.password
    })
    router.push('/')
  } catch (error) {
    console.error('Registration failed:', error)
    alert('注册失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register {
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