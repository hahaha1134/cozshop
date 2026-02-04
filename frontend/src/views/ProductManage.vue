<template>
  <div class="product-manage">
    <div class="container">
      <h1 class="page-title">我的商品</h1>
      
      <div class="card">
        <div class="card-header">
          <h2>商品管理</h2>
          <router-link to="/product/create" class="btn btn-primary">
            发布新商品
          </router-link>
        </div>
        
        <div class="card-body">
          <div v-if="loading" class="loading">
            <div class="spinner"></div>
          </div>
          
          <div v-else-if="products.length === 0" class="empty-state">
            <div class="empty-state-icon">📦</div>
            <p class="empty-state-text">您还没有发布商品</p>
            <router-link to="/product/create" class="btn btn-primary">
              发布商品
            </router-link>
          </div>
          
          <div v-else class="products-table">
            <table>
              <thead>
                <tr>
                  <th>商品名称</th>
                  <th>分类</th>
                  <th>价格</th>
                  <th>库存</th>
                  <th>状态</th>
                  <th>发布时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="product in products" :key="product.id">
                  <td class="product-name">
                    <div class="product-info">
                      <img :src="product.image" :alt="product.name" class="product-thumbnail" />
                      <span>{{ product.name }}</span>
                    </div>
                  </td>
                  <td>{{ product.category }}</td>
                  <td>¥{{ product.price.toFixed(2) }}</td>
                  <td>{{ product.stock }}</td>
                  <td>
                    <span class="status-badge" :class="product.stock > 0 ? 'in-stock' : 'out-of-stock'">
                      {{ product.stock > 0 ? '在售' : '缺货' }}
                    </span>
                  </td>
                  <td>{{ formatDate(product.created_at) }}</td>
                  <td class="actions">
                    <button 
                      class="btn btn-secondary btn-sm" 
                      @click="editProduct(product)"
                    >
                      编辑
                    </button>
                    <button 
                      class="btn btn-danger btn-sm" 
                      @click="deleteProduct(product.id)"
                    >
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/utils/api'

const router = useRouter()
const loading = ref(true)
const products = ref([])

const fetchProducts = async () => {
  loading.value = true
  try {
    const response = await api.get('/products/my')
    products.value = response.data
  } catch (error) {
    console.error('Failed to fetch products:', error)
  } finally {
    loading.value = false
  }
}

const editProduct = (product) => {
  router.push(`/product/edit/${product.id}`)
}

const deleteProduct = async (productId) => {
  if (confirm('确定要删除这个商品吗？')) {
    try {
      console.log('Deleting product:', productId)
      const response = await api.delete(`/products/${productId}`)
      console.log('Delete response:', response)
      await fetchProducts()
      console.log('Products fetched after delete')
      alert('商品删除成功！')
    } catch (error) {
      console.error('Failed to delete product:', error)
      console.error('Error details:', error.response)
      alert('删除失败，请重试')
    }
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.product-manage {
  padding: 40px 0;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 32px;
  color: var(--text-primary);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
}

.card-header h2 {
  font-size: 20px;
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
}

.card-body {
  padding: 24px;
}

.products-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

th {
  background-color: var(--bg-secondary);
  font-weight: 600;
  color: var(--text-primary);
}

.product-name {
  min-width: 250px;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.product-thumbnail {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.in-stock {
  background: #c6f6d5;
  color: #22543d;
}

.status-badge.out-of-stock {
  background: #fed7d7;
  color: #742a2a;
}

.actions {
  display: flex;
  gap: 8px;
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .card-body {
    padding: 20px;
  }
  
  table {
    font-size: 14px;
  }
  
  th, td {
    padding: 12px;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .actions .btn {
    width: 100%;
  }
}
</style>