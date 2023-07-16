const Layout = () => import('@/layout/index.vue')
const system = () => import('@/views/system/index.vue')

export default [
  {
    path: '/system',
    component: Layout,
    name: 'system',
    meta: {
      title: '系统管理',
    },
    icon: 'Tools',
    alwaysShow: true,
    children: [
      {
        path: '',
        name: 'setting',
        component: system,
        meta: {
          title: '股票更新',
        },
      },
    ],
  },
]
