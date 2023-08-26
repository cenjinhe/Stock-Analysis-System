import request from '@/utils/request'

// 获取股票列表
export const getStockList = params => {
  return request({
    url: '/api/stockManage/getStockList/',
    method: 'get',
    params,
  })
}

// 更新股票(深市/沪市)
export const updateStockList = data => {
  return request({
    url: '/api/stockManage/updateStockList/',
    method: 'post',
    timeout: 1000 * 60 * 60, // 1小时
    data,
  })
}
