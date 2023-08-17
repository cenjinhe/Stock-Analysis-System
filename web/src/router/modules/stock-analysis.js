const Layout = () => import('@/layout/index.vue')
const stock_analysis = () => import('@/views/stock-analysis/index.vue')

export default [
  {
    path: '/stock-analysis',
    component: Layout,
    name: 'stock-analysis',
    meta: {
      title: '股票分析',
    },
    icon: 'TrendCharts',
    alwaysShow: true,
    children: [
      {
        path: '',
        name: 'analysis',
        component: stock_analysis,
        meta: {
          title: '选股策略',
        },
      },
    ],
  },
]
