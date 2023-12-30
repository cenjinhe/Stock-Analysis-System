const Layout = () => import('@/layout/index.vue')
const StockList = () => import('@/views/stock-manage/stock-list/index.vue')
const Trend = () => import('@/views/stock-manage/trend/index.vue')
const stock_analysis = () => import('@/views/stock-analysis/index.vue')
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
    // icon: 'TrendCharts',
    alwaysShow: true,
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
      {
        path: 'stock-analysis',
        name: 'analysis',
        component: stock_analysis,
        meta: {
          title: '选股策略',
        },
      },
      {
        path: 'stock-analysis',
        name: 'analysis',
        component: stock_analysis,
        meta: {
          title: '自动选股',
        },
      },
      {
        path: 'stock-analysis',
        name: 'analysis',
        component: stock_analysis,
        meta: {
          title: '交易管理',
        },
      },
    ],
  },
]
