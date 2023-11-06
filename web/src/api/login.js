/*
 * @Description:
 * @version:
 * @Date: 2021-04-20 11:06:21
 * @LastEditors: cenjinhe@126.com
 * @LastEditTime: 2021-04-21 09:36:55
 * @Author: cenjinhe@126.com
 * @HomePage: https://cenjinhe.gitee.io/Stock-System
 * @Github: https://github.com/cenjinhe/Stock-System
 * @Donate: https://cenjinhe.gitee.io/Stock-System/donate/
 */
import request from '@/utils/request'

// 登录接口
export const Login = data => {
  return request({
    url: '/api/user/login/',
    method: 'post',
    data,
  })
}

// 获取登录用户信息
export const GetUserinfo = () => {
  return request({
    // url: '/api/user/userinfo/',
    url: '/api/userinfo/',
    method: 'get',
  })
}
