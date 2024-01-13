const Layout = () => import('@/layout/index.vue')
const StockSelect = () => import('@/views/stock-select/index.vue')

export default [
  {
    path: '/stock-select',
    component: Layout,
    name: 'StockSelect',
    meta: {
      title: '推荐股票',
    },
    icon: 'icon-recommend2',
    children: [
      {
        path: '',
        component: StockSelect,
        meta: {
          title: '筛选股票',
        },
      },
    ],
  },
]
