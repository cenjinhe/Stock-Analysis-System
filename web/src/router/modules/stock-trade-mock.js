const Layout = () => import('@/layout/index.vue')
const StockTrade = () => import('@/views/stock-trade-mock/index.vue')

export default [
  {
    path: '/auto-trade-mock',
    component: Layout,
    name: 'auto-trade-mock',
    meta: {
      title: '模拟交易',
    },
    icon: 'icon-test',
    children: [
      {
        path: '',
        component: StockTrade,
        meta: {
          title: '模拟交易',
        },
      },
    ],
  },
]
