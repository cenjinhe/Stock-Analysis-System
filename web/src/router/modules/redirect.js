/*
 * @Description:
 * @version:
 * @Date: 2021-04-20 11:06:21
 * @LastEditors: cenjinhe@126.com
 * @LastEditTime: 2021-04-21 09:34:40
 * @Author: cenjinhe@126.com
 * @HomePage: https://cenjinhe.gitee.io/Stock-Analysis-System
 * @Github: https://github.com/cenjinhe/Stock-Analysis-System
 * @Donate: https://cenjinhe.gitee.io/Stock-Analysis-System/donate/
 */
const Layout = () => import('@/layout/index.vue')
const Redirect = () => import('@/views/redirect/index.vue')

export default [
  {
    path: '/redirect/:path(.*)',
    component: Layout,
    children: [
      {
        path: '',
        component: Redirect,
      },
    ],
  },
]
