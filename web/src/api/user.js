import request from '@/utils/request'

// 获取用户列表
export const getUserInfoList = params => {
  return request({
    url: '/api/user/getUserInfoList/',
    method: 'get',
    params,
  })
}

// 添加用户
export const addUserInfo = data => {
  return request({
    url: '/api/user/addUserInfo/',
    method: 'post',
    data,
  })
}
