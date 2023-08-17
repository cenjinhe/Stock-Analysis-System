const Layout = () => import('@/layout/index.vue')
const AutoTrade = () => import('@/views/auto-trade/index.vue')

export default [
  {
    path: '/auto-trade',
    component: Layout,
    name: 'auto-trade',
    meta: {
      title: '自动交易',
    },
    icon: 'Platform',
    children: [
      {
        path: '',
        component: AutoTrade,
        meta: {
          title: '自动交易',
        },
      },
    ],
  },
]
