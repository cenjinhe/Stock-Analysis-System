const Layout = () => import('@/layout/index.vue')
const IndicatorFormula = () => import('@/views/stock-about/indicator-formula/index.vue')

export default [
  {
    path: '/stock-about',
    component: Layout,
    name: 'stockAbout',
    meta: {
      title: '关于我们',
    },
    icon: 'Location',
    alwaysShow: true,
    children: [
      {
        path: 'indicator-formula',
        name: 'IndicatorFormula',
        component: IndicatorFormula,
        meta: {
          title: '指标公式',
        },
      },
    ],
  },
]
