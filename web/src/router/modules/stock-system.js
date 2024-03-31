const Layout = () => import('@/layout/index.vue')
const StockTrade = () => import('@/views/stock-trade/index.vue')

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
        component: StockTrade,
        meta: { title: '系统配置' },
      },
    ],
  },
]
