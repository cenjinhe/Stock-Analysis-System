const Layout = () => import('@/layout/index.vue')
const StockTrade = () => import('@/views/auto-trade/index.vue')

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
        component: StockTrade,
        meta: {
          title: '自动交易',
        },
      },
    ],
  },
]
