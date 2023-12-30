import request from '@/utils/request'

// 获取最近上升趋势变化的数据列表
export const getUpTrendDataList = params => {
  return request({
    url: '/api/stockManage/getUpTrendDataList/',
    method: 'get',
    params,
  })
}

// 更新股票分析结果-斜率状态
export const postUpdateTrendStatus = data => {
  return request({
    url: '/api/stockManage/postUpdateTrendStatus/',
    method: 'post',
    data,
  })
}
