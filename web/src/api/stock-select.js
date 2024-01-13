import request from '@/utils/request'

export const postUpdateStockSelect = data => {
  return request({
    url: '/api/stockManage/postUpdateStockSelect/',
    method: 'post',
    data,
  })
}
