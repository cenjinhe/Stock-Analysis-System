import request from '@/utils/request'

// 更新config
export const putUpdateConfig = data => {
  return request({
    url: '/api/stockManage/putUpdateConfig/',
    method: 'put',
    data,
  })
}

// 获取config
export const getConfigValue = params => {
  return request({
    url: '/api/stockManage/getConfigValue/',
    method: 'get',
    params,
  })
}