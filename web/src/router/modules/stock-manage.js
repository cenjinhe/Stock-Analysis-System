const Layout = () => import('@/layout/index.vue')
const stock_analysis = () => import('@/views/stock-analysis/index.vue')
const StockUpdate = () => import('@/views/stock-manage/history-data/index.vue')

export default [
  {
    path: '/stock-manage',
    component: Layout,
    name: 'stockManage',
    meta: {
      title: '数据管理',
    },
    icon: 'Management',
    // icon: 'TrendCharts',
    // alwaysShow: true,
    children: [
      {
        path: 'history-data',
        name: 'HistoryData',
        component: StockUpdate,
        meta: {
          title: '历史数据-证券宝',
        },
      },
      {
        path: 'history-data2',
        name: 'HistoryData2',
        component: StockUpdate,
        meta: {
          title: '历史数据-同花顺',
        },
      },
    ],
  },
]
