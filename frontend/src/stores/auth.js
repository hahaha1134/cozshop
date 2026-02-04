import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  const setAuth = (authData) => {
    token.value = authData.access_token
    user.value = authData.user
    localStorage.setItem('token', authData.access_token)
    localStorage.setItem('user', JSON.stringify(authData.user))
  }

  const clearAuth = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const login = async (credentials) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/auth/login', credentials)
      setAuth(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '登录失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const register = async (userData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/auth/register', userData)
      setAuth(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '注册失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    clearAuth()
  }

  const fetchProfile = async () => {
    if (!token.value) return
    
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/auth/profile')
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '获取用户信息失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout,
    fetchProfile
  }
})