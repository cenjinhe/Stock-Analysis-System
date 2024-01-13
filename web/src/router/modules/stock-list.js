const Layout = () => import('@/layout/index.vue')
const StockList = () => import('@/views/stock-list/index.vue')

export default [
  {
    path: '/stock-list',
    component: Layout,
    name: 'stock-list',
    meta: {
      title: '股票列表',
    },
    icon: 'icon-trend',
    children: [
      {
        path: 'list',
        name: 'stockList',
        component: StockList,
        meta: {
          title: '股票列表',
          keepAlive: true,
        },
      },
    ],
  },
]
