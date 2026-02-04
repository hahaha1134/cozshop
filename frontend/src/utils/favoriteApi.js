import api from './api'

export const favoriteApi = {
  // 获取用户的收藏列表
  getFavorites: async () => {
    try {
      const response = await api.get('/favorites')
      return response.data
    } catch (error) {
      console.error('获取收藏列表失败:', error)
      throw error
    }
  },
  
  // 添加收藏
  addToFavorites: async (productId) => {
    try {
      const response = await api.post('/favorites', { product_id: productId })
      return response.data
    } catch (error) {
      console.error('添加收藏失败:', error)
      throw error
    }
  },
  
  // 移除收藏
  removeFromFavorites: async (productId) => {
    try {
      const response = await api.delete(`/favorites/${productId}`)
      return response.data
    } catch (error) {
      console.error('移除收藏失败:', error)
      throw error
    }
  },
  
  // 检查商品是否已收藏
  checkFavorite: async (productId) => {
    try {
      const response = await api.get(`/favorites/check/${productId}`)
      return response.data
    } catch (error) {
      console.error('检查收藏状态失败:', error)
      throw error
    }
  }
}
