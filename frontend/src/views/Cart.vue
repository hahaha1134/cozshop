<template>
  <div class="cart">
    <div class="container">
      <h1 class="page-title">购物车</h1>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="cartStore.isEmpty" class="empty-state">
        <div class="empty-state-icon">🛒</div>
        <p class="empty-state-text">购物车是空的</p>
        <router-link to="/" class="btn btn-primary">去购物</router-link>
      </div>
      
      <div v-else class="cart-content">
        <div class="cart-items">
          <div 
            v-for="item in cartStore.items" 
            :key="item.product_id"
            class="cart-item card"
          >
            <img :src="item.image" :alt="item.name" class="item-image" />
            <div class="item-details">
              <h3 class="item-name">{{ item.name }}</h3>
              <p class="item-price">¥{{ item.price.toFixed(2) }}</p>
            </div>
            <div class="item-quantity">
              <button 
                class="btn btn-secondary btn-sm"
                @click="updateQuantity(item.product_id, item.quantity - 1)"
                :disabled="item.quantity <= 1"
              >-</button>
              <span class="quantity-value">{{ item.quantity }}</span>
              <button 
                class="btn btn-secondary btn-sm"
                @click="updateQuantity(item.product_id, item.quantity + 1)"
              >+</button>
            </div>
            <div class="item-total">
              <span class="total-price">¥{{ (item.price * item.quantity).toFixed(2) }}</span>
              <button 
                class="btn btn-danger btn-sm"
                @click="removeFromCart(item.product_id)"
              >删除</button>
            </div>
          </div>
        </div>
        
        <div class="cart-summary card">
          <h2 class="summary-title">订单摘要</h2>
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
          <button 
            class="btn btn-primary btn-lg"
            @click="checkout"
            :disabled="cartStore.isEmpty"
          >
            去结算
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const cartStore = useCartStore()

const loading = ref(true)

const updateQuantity = async (productId, quantity) => {
  try {
    await cartStore.updateQuantity(productId, quantity)
  } catch (error) {
    console.error('Failed to update quantity:', error)
    alert('更新数量失败，请重试')
  }
}

const removeFromCart = async (productId) => {
  if (confirm('确定要删除这个商品吗？')) {
    try {
      await cartStore.removeFromCart(productId)
    } catch (error) {
      console.error('Failed to remove item:', error)
      alert('删除失败，请重试')
    }
  }
}

const checkout = () => {
  router.push('/orders')
}

onMounted(async () => {
  try {
    console.log('Fetching cart data...')
    await cartStore.fetchCart()
    console.log('Cart data fetched successfully:', cartStore.items)
  } catch (error) {
    console.error('Failed to fetch cart:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.cart {
  padding: 40px 0;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 32px;
  color: var(--text-primary);
}

.cart-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cart-item {
  display: grid;
  grid-template-columns: auto 2fr auto auto;
  gap: 20px;
  align-items: center;
  padding: 20px;
}

.item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
}

.item-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.item-name {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.item-price {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.item-quantity {
  display: flex;
  align-items: center;
  gap: 8px;
}

.quantity-value {
  min-width: 30px;
  text-align: center;
  font-weight: 600;
}

.item-total {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.total-price {
  font-size: 18px;
  font-weight: 700;
  color: var(--primary-color);
}

.cart-summary {
  padding: 24px;
  position: sticky;
  top: 100px;
  height: fit-content;
}

.summary-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color);
  font-size: 16px;
}

.summary-row.total {
  border-bottom: none;
  border-top: 2px solid var(--border-color);
  font-size: 20px;
  font-weight: 700;
  margin-top: 12px;
  padding-top: 20px;
}

.summary-row.total span:last-child {
  color: var(--primary-color);
}

.cart-summary .btn {
  width: 100%;
  margin-top: 24px;
}

@media (max-width: 768px) {
  .cart-content {
    grid-template-columns: 1fr;
  }
  
  .cart-item {
    grid-template-columns: auto 1fr;
    gap: 12px;
  }
  
  .item-quantity {
    grid-column: 2;
  }
  
  .item-total {
    grid-column: 2;
    align-items: flex-start;
  }
}
</style>