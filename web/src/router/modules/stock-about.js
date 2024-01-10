const Layout = () => import('@/layout/index.vue')
const MA = () => import('@/views/stock-about/indicator-formula/component/MA.vue')
const MACD = () => import('@/views/stock-about/indicator-formula/component/MACD.vue')
const IndicatorFormula = () => import('@/views/stock-about/indicator-formula/index.vue')
const BaoStock = () => import('@/views/stock-about/baostock/index.vue')

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
        children: [
          {
            path: 'MA',
            name: 'MA',
            component: MA,
            meta: {
              title: 'MA',
            },
            hidden: true,
          },
          {
            path: 'MACD',
            name: 'MACD',
            component: MACD,
            meta: {
              title: 'MACD',
            },
            hidden: true,
          },
        ],
      },
      {
        path: 'bao-stock',
        name: 'BaoStock',
        component: BaoStock,
        meta: {
          title: '证券宝官网',
        },
      },
    ],
  },
]
