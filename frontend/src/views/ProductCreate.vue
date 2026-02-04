<template>
  <div class="product-create">
    <div class="container">
      <h1 class="page-title">发布商品</h1>
      
      <div class="card">
        <form @submit.prevent="handleSubmit" class="product-form">
          <div class="form-section">
            <h2>基本信息</h2>
            
            <div class="form-group">
              <label for="name">商品名称</label>
              <input 
                id="name" 
                v-model="formData.name" 
                type="text" 
                required 
                placeholder="请输入商品名称"
              />
            </div>
            
            <div class="form-group">
              <label for="category">商品分类</label>
              <select id="category" v-model="formData.category" required>
                <option value="">请选择分类</option>
                <option value="Electronics">数码产品</option>
                <option value="Clothing">服装配饰</option>
                <option value="Books">书籍教育</option>
                <option value="Home">家居用品</option>
                <option value="Other">其他</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="price">价格</label>
              <input 
                id="price" 
                v-model.number="formData.price" 
                type="number" 
                step="0.01" 
                min="0.01" 
                required 
                placeholder="请输入价格"
              />
            </div>
            
            <div class="form-group">
              <label for="stock">库存</label>
              <input 
                id="stock" 
                v-model.number="formData.stock" 
                type="number" 
                min="1" 
                required 
                placeholder="请输入库存"
              />
            </div>
            
            <div class="form-group">
              <label for="condition">新旧程度</label>
              <select id="condition" v-model="formData.condition" required>
                <option value="">请选择新旧程度</option>
                <option value="new">全新</option>
                <option value="9">9成新</option>
                <option value="8">8成新</option>
                <option value="7">7成新</option>
                <option value="6">6成新及以下</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="tradeMethod">交易方式</label>
              <select id="tradeMethod" v-model="formData.tradeMethod" required>
                <option value="">请选择交易方式</option>
                <option value="self">自取</option>
                <option value="both">自取/邮寄</option>
              </select>
            </div>
          </div>
          
          <div class="form-section">
            <h2>商品详情</h2>
            
            <div class="form-group">
              <label for="description">商品描述</label>
              <textarea 
                id="description" 
                v-model="formData.description" 
                rows="6" 
                required 
                placeholder="请详细描述商品，包括品牌、规格、使用情况等"
              ></textarea>
            </div>
            
            <div class="form-group">
              <label for="image">商品图片</label>
              <input 
                id="image" 
                type="text" 
                v-model="formData.image" 
                placeholder="请输入图片URL"
              />
              <p class="form-hint">可以使用图片托管服务获取图片URL</p>
            </div>
          </div>
          
          <div class="form-section">
            <h2>交易信息</h2>
            
            <div class="form-group">
              <label for="tradeAddress">交易地址</label>
              <input 
                id="tradeAddress" 
                v-model="formData.tradeAddress" 
                type="text" 
                required 
                placeholder="请输入交易地址"
              />
            </div>
          </div>
          
          <div class="form-actions">
            <button 
              type="submit" 
              class="btn btn-primary btn-lg" 
              :disabled="loading"
            >
              {{ loading ? '发布中...' : '发布商品' }}
            </button>
            <router-link to="/profile" class="btn btn-secondary btn-lg">
              取消
            </router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/utils/api'

const router = useRouter()
const loading = ref(false)

const formData = ref({
  name: '',
  description: '',
  price: 0,
  category: '',
  stock: 1,
  image: 'https://via.placeholder.com/300x300',
  condition: '',
  tradeMethod: '',
  tradeAddress: ''
})

const handleSubmit = async () => {
  loading.value = true
  try {
    const response = await api.post('/products', formData.value)
    alert('商品发布成功！')
    router.push('/profile')
  } catch (error) {
    console.error('Failed to create product:', error)
    alert('发布失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.product-create {
  padding: 40px 0;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 32px;
  color: var(--text-primary);
}

.product-form {
  padding: 32px;
}

.form-section {
  margin-bottom: 40px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border-color);
}

.form-section h2 {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 24px;
  color: var(--text-primary);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.form-group textarea {
  resize: vertical;
  min-height: 120px;
}

.form-hint {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.form-actions {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
  margin-top: 40px;
}

@media (max-width: 768px) {
  .product-form {
    padding: 20px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions .btn {
    width: 100%;
  }
}
</style>