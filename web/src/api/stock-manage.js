import request from '@/utils/request'

// 获取股票列表
export const getStockList = data => {
  return request({
    url: '/api/stockManage/getStockList/',
    method: 'get',
    data,
  })
}
