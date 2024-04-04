const Layout = () => import('@/layout/index.vue')
const System = () => import('@/views/system/index.vue')

export default [
  {
    path: '/stock-system',
    component: Layout,
    name: 'stock-system',
    meta: { title: '系统配置' },
    icon: 'Setting',
    children: [
      {
        path: '',
        component: System,
        meta: { title: '系统配置' },
      },
    ],
  },
]
