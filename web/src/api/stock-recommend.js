import request from '@/utils/request'

export const postUpdateStockRecommend = data => {
  return request({
    url: '/api/stockManage/postUpdateStockRecommend/',
    method: 'post',
    timeout: 1000 * 60 * 60 * 24, // 24Сʱ
    data,
  })
}
