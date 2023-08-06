const Layout = () => import('@/layout/index.vue')
const StockList = () => import('@/views/stock-manage/stock-list/index.vue')

export default [
  {
    path: '/stock-manage',
    component: Layout,
    name: 'stock-manage',
    meta: {
      title: '股票管理',
    },
    icon: 'Management',
    alwaysShow: true,
    children: [
      {
        path: 'stock-list',
        component: StockList,
        meta: {
          title: '股票列表',
        },
      },
    ],
  },
]
