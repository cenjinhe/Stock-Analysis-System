const Layout = () => import('@/layout/index.vue')
const Trend = () => import('@/views/stock-trend/index.vue')

export default [
  {
    path: '/stock-trend',
    component: Layout,
    name: 'stockTrend',
    meta: {
      title: '拟合斜率',
    },
    icon: 'Histogram',
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
