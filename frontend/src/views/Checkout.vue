<template>
  <div class="checkout">
    <div class="container">
      <h1 class="page-title">结算</h1>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="cartStore.isEmpty" class="empty-state">
        <div class="empty-state-icon">🛒</div>
        <p class="empty-state-text">购物车是空的</p>
        <router-link to="/" class="btn btn-primary">去购物</router-link>
      </div>
      
      <div v-else class="checkout-content">
        <div class="checkout-items card">
          <h2 class="section-title">订单商品</h2>
          <div 
            v-for="item in cartStore.items" 
            :key="item.product_id"
            class="checkout-item"
          >
            <img :src="item.image" :alt="item.name" class="item-image" />
            <div class="item-details">
              <h3 class="item-name">{{ item.name }}</h3>
              <p class="item-price">¥{{ item.price.toFixed(2) }} × {{ item.quantity }}</p>
            </div>
            <span class="item-total">¥{{ (item.price * item.quantity).toFixed(2) }}</span>
          </div>
          
          <div class="checkout-summary">
            <div class="summary-row">
              <span>商品数量:</span>
              <span>{{ cartStore.totalItems }} 件</span>
            </div>
            <div class="summary-row">
              <span>小计:</span>
              <span>¥{{ cartStore.totalPrice.toFixed(2) }}</span>
            </div>
            <div class="summary-row">
              <span>运费:</span>
              <span>¥0.00</span>
            </div>
            <div class="summary-row total">
              <span>总计:</span>
              <span>¥{{ cartStore.totalPrice.toFixed(2) }}</span>
            </div>
          </div>
        </div>
        
        <div class="checkout-form card">
          <h2 class="section-title">收货信息</h2>
          <form @submit.prevent="handleCheckout">
            <div class="form-group">
              <label for="address">收货地址</label>
              <textarea
                id="address"
                v-model="orderData.shippingAddress.address"
                required
                placeholder="请输入详细地址"
                rows="3"
              ></textarea>
            </div>
            
            <div class="form-group">
              <label for="city">城市</label>
              <input
                id="city"
                v-model="orderData.shippingAddress.city"
                type="text"
                required
                placeholder="请输入城市"
              />
            </div>
            
            <div class="form-group">
              <label for="postalCode">邮编</label>
              <input
                id="postalCode"
                v-model="orderData.shippingAddress.postalCode"
                type="text"
                required
                placeholder="请输入邮编"
              />
            </div>
            
            <div class="form-group">
              <label for="country">国家</label>
              <input
                id="country"
                v-model="orderData.shippingAddress.country"
                type="text"
                required
                placeholder="请输入国家"
              />
            </div>
            
            <div class="form-group">
              <label for="paymentMethod">支付方式</label>
              <select
                id="paymentMethod"
                v-model="orderData.paymentMethod"
                required
              >
                <option value="Credit Card">信用卡</option>
                <option value="PayPal">PayPal</option>
                <option value="Bank Transfer">银行转账</option>
              </select>
            </div>
            
            <button 
              type="submit" 
              class="btn btn-primary btn-lg"
              :disabled="submitting"
            >
              {{ submitting ? '提交中...' : '提交订单' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import api from '@/utils/api'

const router = useRouter()
const cartStore = useCartStore()

const loading = ref(true)
const submitting = ref(false)

const orderData = ref({
  shippingAddress: {
    address: '',
    city: '',
    postalCode: '',
    country: ''
  },
  paymentMethod: 'Credit Card'
})

const handleCheckout = async () => {
  submitting.value = true
  try {
    const response = await api.post('/orders', orderData.value)
    
    await cartStore.clearCart()
    router.push(`/orders`)
  } catch (error) {
    console.error('Checkout failed:', error)
    alert('提交订单失败，请重试')
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  try {
    await cartStore.fetchCart()
  } catch (error) {
    console.error('Failed to fetch cart:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.checkout {
  padding: 40px 0;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 32px;
  color: var(--text-primary);
}

.checkout-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.checkout-items {
  padding: 24px;
}

.checkout-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid var(--border-color);
}

.checkout-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
}

.item-details {
  flex: 1;
}

.item-name {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 4px 0;
  color: var(--text-primary);
}

.item-price {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.item-total {
  font-weight: 600;
  color: var(--text-primary);
}

.checkout-summary {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 2px solid var(--border-color);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  font-size: 16px;
}

.summary-row.total {
  border-top: 1px solid var(--border-color);
  font-size: 20px;
  font-weight: 700;
  margin-top: 12px;
  padding-top: 20px;
}

.summary-row.total span:last-child {
  color: var(--primary-color);
}

.checkout-form {
  padding: 24px;
  position: sticky;
  top: 100px;
  height: fit-content;
}

.checkout-form form {
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

.form-group input,
.form-group textarea {
  padding: 12px 16px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  font-size: 16px;
  font-family: inherit;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

@media (max-width: 768px) {
  .checkout-content {
    grid-template-columns: 1fr;
  }
}
</style>