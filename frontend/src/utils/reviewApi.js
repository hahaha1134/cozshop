import api from './api'

export const reviewApi = {
  // 获取商品评价
  getProductReviews: async (productId) => {
    try {
      const response = await api.get(`/reviews/product/${productId}`)
      return response.data
    } catch (error) {
      console.error('获取商品评价失败:', error)
      throw error
    }
  },
  
  // 创建评价
  createReview: async (reviewData) => {
    try {
      const response = await api.post('/reviews', reviewData)
      return response.data
    } catch (error) {
      console.error('创建评价失败:', error)
      throw error
    }
  },
  
  // 删除评价
  deleteReview: async (reviewId) => {
    try {
      const response = await api.delete(`/reviews/${reviewId}`)
      return response.data
    } catch (error) {
      console.error('删除评价失败:', error)
      throw error
    }
  }
}
