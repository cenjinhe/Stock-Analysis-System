import request from '@/utils/request'

// ��ȡ����������Ʊ仯�������б�
export const getUpTrendDataList = params => {
  return request({
    url: '/api/stockManage/getUpTrendDataList/',
    method: 'get',
    params,
  })
}

// ���¹�Ʊ�������-б��״̬
export const postUpdateTrendStatus = data => {
  return request({
    url: '/api/stockManage/postUpdateTrendStatus/',
    method: 'post',
    data,
  })
}
