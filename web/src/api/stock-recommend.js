import request from '@/utils/request'

// 获取
export const getStockRecommendResults = params => {
  return request({
    url: '/api/stockManage/getStockRecommendResults/',
    method: 'get',
    params,
  })
}
// 更新
export const postUpdateStockRecommend = data => {
  return request({
    url: '/api/stockManage/postUpdateStockRecommend/',
    method: 'post',
    timeout: 1000 * 60 * 60 * 24, // 24 hour
    data,
  })
}
