import request from '@/utils/request'

export const postUpdateStockRecommend = data => {
  return request({
    url: '/api/stockManage/postUpdateStockRecommend/',
    method: 'post',
    data,
  })
}
