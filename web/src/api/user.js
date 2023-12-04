import request from '@/utils/request'

// ��ȡ�û��б�
export const getUserInfoList = params => {
  return request({
    url: '/api/user/getUserInfoList/',
    method: 'get',
    params,
  })
}

// ����û�
export const addUserInfo = data => {
  return request({
    url: '/api/user/addUserInfo/',
    method: 'post',
    data,
  })
}
