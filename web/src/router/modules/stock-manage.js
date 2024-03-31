const Layout = () => import('@/layout/index.vue')
const StockUpdate = () => import('@/views/stock-manage/history-data/index.vue')
const WorkFlow = () => import('@/views/stock-manage/work-flow/index.vue')

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
      {
        path: 'work-flow',
        name: 'WorkFlow',
        component: WorkFlow,
        meta: {
          title: '更新数据-工作流',
        },
      },
    ],
  },
]
