/*
 * @Description:
 * @version:
 * @Date: 2021-04-20 16:35:04
 * @LastEditors: cenjinhe@126.com
 * @LastEditTime: 2022-09-25 11:50:39
 * @Author: cenjinhe@126.com
 * @HomePage: https://cenjinhe.gitee.io/Stock-Analysis-System
 * @Github: https://github.com/cenjinhe/Stock-Analysis-System
 * @Donate: https://cenjinhe.gitee.io/Stock-Analysis-System/donate/
 */
import request from '@/utils/request'

// 测试
export const TestError = () => {
  return request({
    url: '/api/500',
    method: 'get',
  })
}

// 用户列表
export const getUsers = data => {
  return request({
    url: '/api/test/users',
    method: 'post',
    data,
  })
}
