const Layout = () => import('@/layout/index.vue')
const StockRecommend = () => import('@/views/stock-recommend/index.vue')

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
        component: StockRecommend,
        meta: {
          title: '筛选股票',
        },
      },
    ],
  },
]
