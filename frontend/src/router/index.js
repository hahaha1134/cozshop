import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页 - CozShop' }
  },
  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: () => import('@/views/ProductDetail.vue'),
    meta: { title: '商品详情 - CozShop' }
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('@/views/Cart.vue'),
    meta: { title: '购物车 - CozShop', requiresAuth: true }
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('@/views/Orders.vue'),
    meta: { title: '我的订单 - CozShop', requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { title: '个人中心 - CozShop', requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录 - CozShop', guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { title: '注册 - CozShop', guest: true }
  },
  {
    path: '/product/create',
    name: 'ProductCreate',
    component: () => import('@/views/ProductCreate.vue'),
    meta: { title: '发布商品 - CozShop', requiresAuth: true }
  },
  {
    path: '/product/manage',
    name: 'ProductManage',
    component: () => import('@/views/ProductManage.vue'),
    meta: { title: '商品管理 - CozShop', requiresAuth: true }
  },
  {
    path: '/product/edit/:id',
    name: 'ProductEdit',
    component: () => import('@/views/ProductEdit.vue'),
    meta: { title: '编辑商品 - CozShop', requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/Admin.vue'),
    meta: { title: '管理后台 - CozShop', requiresAuth: true }
  },
  {
    path: '/admin/products',
    name: 'AdminProducts',
    component: () => import('@/views/AdminProducts.vue'),
    meta: { title: '商品管理 - CozShop', requiresAuth: true }
  },
  {
    path: '/admin/orders',
    name: 'AdminOrders',
    component: () => import('@/views/AdminOrders.vue'),
    meta: { title: '订单管理 - CozShop', requiresAuth: true }
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: () => import('@/views/Favorites.vue'),
    meta: { title: '我的收藏 - CozShop', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Update page title
  document.title = to.meta.title || 'CozShop - 现代电商平台'
  
  // Check auth requirements
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router