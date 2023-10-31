/*
 * @Description:
 * @version:
 * @Date: 2021-04-20 11:06:21
 * @LastEditors: cenjinhe@126.com
 * @LastEditTime: 2021-07-26 13:37:30
 * @Author: cenjinhe@126.com
 * @HomePage: https://cenjinhe.gitee.io/Stock-System
 * @Github: https://github.com/cenjinhe/Stock-System
 * @Donate: https://cenjinhe.gitee.io/Stock-System/donate/
 */
import request from '@/utils/request'

// 获取菜单
export const GetMenus = params => {
  return request({
    url: '/api/menus',
    method: 'get',
    params,
  })
}
