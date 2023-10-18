const Layout = () => import('@/layout/index.vue')
const StockList = () => import('@/views/stock-manage/stock-list/index.vue')
const StockUpdate = () => import('@/views/stock-manage/history-data/index.vue')

export default [
  {
    path: '/stock-manage',
    component: Layout,
    name: 'stockManage',
    meta: {
      title: '股票管理',
    },
    icon: 'Management',
    alwaysShow: true,
    children: [
      {
        path: 'stock-list',
        name: 'stockList',
        component: StockList,
        meta: {
          title: '股票列表',
          keepAlive: true,
        },
      },
      {
        path: 'history-data',
        name: 'stockUpdate',
        component: StockUpdate,
        meta: {
          title: '历史数据',
        },
      },
    ],
  },
]
