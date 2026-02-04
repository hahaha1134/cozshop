<template>
  <div class="admin-products">
    <div class="container">
      <div class="page-header">
        <h1>商品管理</h1>
        <router-link to="/admin" class="btn btn-secondary">返回后台首页</router-link>
      </div>
      
      <div class="products-list">
        <div class="search-bar">
          <input 
            v-model="searchQuery" 
            @input="handleSearch" 
            placeholder="按商品名称搜索..."
            class="search-input"
          />
        </div>
        
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
        
        <div v-else-if="filteredProducts.length === 0" class="empty-state">
          <div class="empty-icon">📦</div>
          <p>暂无商品</p>
        </div>
        
        <div v-else class="products-grid">
          <div v-for="product in filteredProducts" :key="product.id" class="product-card">
            <div class="product-image">
              <img :src="product.image" :alt="product.name">
            </div>
            <div class="product-info">
              <h3>{{ product.name }}</h3>
              <p class="product-price">¥{{ product.price.toFixed(2) }}</p>
              <p class="product-stock">库存: {{ product.stock }}</p>
              <p class="product-seller">卖家ID: {{ product.seller_id }}</p>
              <p class="product-status">
                状态: <span :class="['status-badge', `status-${product.status || 'pending'}`]">
                  {{ getStatusText(product.status || 'pending') }}
                </span>
              </p>
              <div class="product-actions">
                <router-link :to="`/product/edit/${product.id}`" class="btn btn-primary btn-sm">
                  编辑
                </router-link>
                <button @click="toggleProductStatus(product.id, product.status !== 'approved')" class="btn btn-warning btn-sm">
                  {{ product.status === 'approved' ? '下架' : '通过' }}
                </button>
                <button @click="toggleProductPin(product.id, !product.is_pinned)" class="btn btn-secondary btn-sm">
                  {{ product.is_pinned ? '取消置顶' : '置顶' }}
                </button>
                <button @click="deleteProduct(product.id)" class="btn btn-danger btn-sm">
                  删除
                </button>
              </div>
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

const authStore = useAuthStore()
const router = useRouter()
const products = ref([])
const loading = ref(true)

onMounted(async () => {
  // Check if user is admin
  if (!authStore.user || authStore.user.role !== 'admin') {
    alert('您没有权限访问此页面')
    router.push('/')
    return
  }
  
  await fetchProducts()
})

const fetchProducts = async () => {
  try {
    const response = await api.get('/products')
    products.value = response.data
  } catch (error) {
    console.error('Failed to fetch products:', error)
    alert('获取商品失败')
  } finally {
    loading.value = false
  }
}

const deleteProduct = async (productId) => {
  if (confirm('确定要删除此商品吗？')) {
    try {
      await api.delete(`/products/${productId}`)
      alert('商品删除成功')
      await fetchProducts()
    } catch (error) {
      console.error('Failed to delete product:', error)
      alert('删除商品失败')
    }
  }
}
</script>

<style scoped>
.admin-products {
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

.products-list {
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

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.product-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform 0.3s, box-shadow 0.3s;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
}

.product-image {
  height: 200px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  padding: 1.5rem;
}

.product-info h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.product-price {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

.product-stock {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.product-seller {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.product-actions {
  display: flex;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .products-grid {
    grid-template-columns: 1fr;
  }
}
</style>
