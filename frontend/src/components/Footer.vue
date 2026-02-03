<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h3 class="footer-title">CozShop</h3>
          <p class="footer-text">现代电商平台，为您提供优质的购物体验</p>
        </div>
        
        <div class="footer-section">
          <h4 class="footer-heading">快速链接</h4>
          <ul class="footer-links">
            <li><router-link to="/">首页</router-link></li>
            <li><router-link to="/cart">购物车</router-link></li>
            <li><router-link to="/orders">我的订单</router-link></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h4 class="footer-heading">客户服务</h4>
          <ul class="footer-links">
            <li><a href="#">帮助中心</a></li>
            <li><a href="#">联系我们</a></li>
            <li><a href="#">退换货政策</a></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h4 class="footer-heading">关于我们</h4>
          <ul class="footer-links">
            <li><a href="#">公司简介</a></li>
            <li><a href="#">加入我们</a></li>
            <li><a href="#">隐私政策</a></li>
          </ul>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; 2024 CozShop. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.footer {
  background: var(--text-primary);
  color: white;
  padding: 40px 0 20px;
  margin-top: auto;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 32px;
  margin-bottom: 32px;
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.footer-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-text {
  color: #a0aec0;
  margin: 0;
  line-height: 1.6;
}

.footer-heading {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: white;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-links a {
  color: #a0aec0;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: white;
}

.footer-bottom {
  border-top: 1px solid #4a5568;
  padding-top: 20px;
  text-align: center;
  color: #a0aec0;
}

.footer-bottom p {
  margin: 0;
}
</style>