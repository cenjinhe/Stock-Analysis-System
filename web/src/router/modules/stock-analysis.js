const Layout = () => import('@/layout/index.vue')
const Trend = () => import('@/views/stock-analysis/stock-trend/index.vue')

export default [
  {
    path: '/data-analysis',
    component: Layout,
    name: 'dataAnalysis',
    meta: {
      title: '数据分析',
    },
    icon: 'DataAnalysis',
    alwaysShow: true,
    children: [
      {
        path: 'trend',
        name: 'trend',
        component: Trend,
        meta: {
          title: '拟合斜率',
        },
      },
    ],
  },
]
