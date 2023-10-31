/*
 * @Description:
 * @version:
 * @Date: 2021-04-20 11:06:21
 * @LastEditors: cenjinhe@126.com
 * @LastEditTime: 2022-09-24 19:27:21
 * @Author: cenjinhe@126.com
 * @HomePage: https://cenjinhe.gitee.io/Stock-System
 * @Github: https://github.com/cenjinhe/Stock-System
 * @Donate: https://cenjinhe.gitee.io/Stock-System/donate/
 */
// home.js
const Layout = () => import('@/layout/index.vue')
const Home = () => import('@/views/home/index.vue')

export default [
  {
    path: '/home',
    component: Layout,
    name: 'Dashboard',
    meta: {
      title: '首页',
    },
    icon: 'icon-home',
    children: [
      {
        path: '',
        name: 'home',
        component: Home,
        meta: {
          title: '首页',
          affix: true,
        },
      },
    ],
  },
]
