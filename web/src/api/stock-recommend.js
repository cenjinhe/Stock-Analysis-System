import request from '@/utils/request'

// 获取
export const getStockRecommendResults = params => {
  return request({
    url: '/api/stockManage/getStockRecommendResults/',
    method: 'get',
    params,
  })
}
// 更新数据
export const postUpdateStockRecommend = data => {
  return request({
    url: '/api/stockManage/postUpdateStockRecommend/',
    method: 'post',
    timeout: 1000 * 60 * 60 * 24, // 24 hour
    data,
  })
}

// 更新当前收盘价
export const postUpdateCurrentClose = data => {
  return request({
    url: '/api/stockManage/postUpdateCurrentClose/',
    method: 'post',
    timeout: 1000 * 60 * 60 * 24, // 24 hour
    data,
  })
}

