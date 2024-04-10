import request from '@/utils/request'

// ����config
export const putUpdateConfig = data => {
  return request({
    url: '/api/stockManage/putUpdateConfig/',
    method: 'put',
    data,
  })
}

// ��ȡconfig
export const getConfigValue = params => {
  return request({
    url: '/api/stockManage/getConfigValue/',
    method: 'get',
    params,
  })
}