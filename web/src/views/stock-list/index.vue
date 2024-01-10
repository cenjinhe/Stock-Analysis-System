<template>
  <div>
    <keep-alive>
      <pro-table
        v-if="pageShow === 'stock-list'"
        ref="table"
        :title="`${currentMarket === 1 ? '深市' : '沪市'}股票列表`"
        :request="getList"
        :columns="columns"
        :search="searchConfig"
        :cell-style="cellStyle"
        @selectionChange="handleSelectionChange"
        @sort-change="changeTableSort"
      >
        <!-- 工具栏 -->
        <template #toolbar>
          <el-button icon="Download" type="primary">
            导出Excel
          </el-button>
          <el-button icon="Refresh" style="margin-right: 30px;" @click="refresh">
            刷新
          </el-button>
        </template>
        <template #close="scope">
          <div :style="{color: getCloseColor(scope.row)}">{{scope.row.close}}</div>
        </template>
        <template #ratio="scope">
          <div :style="{color: getCloseColor(scope.row)}">{{ scope.row.ratio }}%</div>
        </template>
        <template #pre_trend_status="{row}">
          <div :style="{color: getTrendStatusColor(row, 'pre_trend_status')}">{{ row.pre_trend_status }}</div>
        </template>
        <template #trend_status="{row}">
          <div :style="{color: getTrendStatusColor(row, 'trend_status')}">{{ row.trend_status }}</div>
        </template>
        <template #trade_status="{row}">
          <el-tag :type="row.trade_status === 1 ? 'success' : 'error'">
            {{ row.trade_status === 1 ? '正常' : '停牌' }}
          </el-tag>
        </template>
        <template #operate="scope">
          <el-button size="small" type="success" @click="btnViewData(scope.row)">查看指标</el-button>
        </template>
      </pro-table>
    </keep-alive>
    <view-data
      v-if="pageShow === 'view-data'"
      v-model:pageShow="pageShow"
      v-model:row="row"
    />
  </div>
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from 'vue'
import { getStockList } from '@/api/stock-manage'
import ViewData from '@/views/stock-list/component/ViewData.vue'

export default defineComponent({
  name: 'stockList',
  components: { ViewData },
  setup() {
    // const { proxy } = getCurrentInstance()

    const state = reactive({
      // 表格列配置，大部分属性跟el-table-column配置一样
      columns: [
        // { type: 'selection', width: 56 },
        {
          label: 'ID',
          prop: 'id',
          minWidth: 60,
        },
        {
          label: 'A股代码',
          prop: 'code',
          minWidth: 120,
          sortable: 'custom',
        },
        {
          label: 'A股简称',
          prop: 'name',
          minWidth: 120,
        },
        {
          label: '上市日期',
          prop: 'listing_date',
          minWidth: 120,
        },
        {
          label: '行情日期',
          prop: 'date',
          minWidth: 120,
        },
        {
          label: '昨日收盘价',
          prop: 'pre_close',
          minWidth: 100,
        },
        {
          label: '现价',
          prop: 'close',
          minWidth: 100,
          tdSlot: 'close',
          sortable: 'custom',
        },
        {
          label: '涨跌幅',
          prop: 'ratio',
          minWidth: 100,
          tdSlot: 'ratio',
          sortable: 'custom',
        },
        {
          label: '斜率',
          prop: 'slope',
          minWidth: 100,
          sortable: 'custom',
        },
        {
          label: '前回趋势',
          prop: 'pre_trend_status',
          minWidth: 110,
          tdSlot: 'pre_trend_status',
          sortable: 'custom',
        },
        {
          label: '当前趋势',
          prop: 'trend_status',
          minWidth: 110,
          tdSlot: 'trend_status',
          // align: 'center',
          sortable: 'custom',
        },
        {
          label: '更新时间',
          prop: 'update_time',
          minWidth: 160,
        },
        {
          label: '交易状态',
          prop: 'trade_status',
          minWidth: 80,
          align: 'center',
          tdSlot: 'trade_status',
          fixed: 'right',
        },
        {
          label: '操作',
          minWidth: 140,
          align: 'center',
          tdSlot: 'operate', // 自定义单元格内容的插槽名称
          fixed: 'right',
        },
      ],
      // 搜索配置
      searchConfig: {
        labelWidth: '90px', // 必须带上单位
        inputWidth: '150px', // 必须带上单位
        fields: [
          {
            type: 'text',
            label: 'A股代码',
            name: 'code',
            defaultValue: '',
          },
          {
            type: 'text',
            label: 'A股简称',
            name: 'name',
            defaultValue: '',
          },
          {
            label: '证券交易所',
            name: 'market',
            type: 'select',
            defaultValue: 1,
            options: [
              {
                name: '深市',
                value: 1,
              },
              {
                name: '沪市',
                value: 0,
              },
            ],
          },
          {
            label: '前回趋势',
            name: 'pre_trend',
            type: 'select',
            defaultValue: 0,
            options: [
              {
                name: '全部',
                value: 0,
              },
              {
                name: '上升',
                value: '上升',
              },
              {
                name: '下降',
                value: '下降',
              },
              {
                name: '平稳',
                value: '平稳',
              },
              {
                name: '波动',
                value: '波动',
              },
            ],
          },
          {
            label: '当前趋势',
            name: 'trend',
            type: 'select',
            defaultValue: 0,
            options: [
              {
                name: '全部',
                value: 0,
              },
              {
                name: '上升',
                value: '上升',
              },
              {
                name: '下降',
                value: '下降',
              },
              {
                name: '平稳',
                value: '平稳',
              },
              {
                name: '波动',
                value: '波动',
              },
            ],
          },
        ],
      },
      // 选择
      selectedItems: [],
      handleSelectionChange(arr) {
        state.selectedItems = arr
      },
      // 排序
      changeTableSort(column) {
        // 获取字段名称和排序类型
        const fieldName = column.prop
        const order = column.order
        // 发起后端请求的接口
        const params = Object.assign(
          table.value.searchModel,
          { column: fieldName },
          { order: order }
        )
        state.getList(params)
        refresh()
      },
      // 设置[现价]列显示的颜色
      getCloseColor(row) {
        if (row.close > row.pre_close) {
          return 'red'
        } else if (row.close < row.pre_close) {
          return 'green'
        } else {
          return ''
        }
      },
      // 设置[斜率状态]列显示的颜色
      getTrendStatusColor(row, field) {
        let status = ''
        switch (field) {
          case 'trend_status': {
            status = row.trend_status
            break
          }
          case 'pre_trend_status': {
            status = row.pre_trend_status
            break
          }
          default:
            break
        }
        if (status === '上升') {
          return 'red'
        } else if (status === '下降') {
          return 'green'
        } else if (status === '波动') {
          return 'blue'
        } else {
          return ''
        }
      },
      // 请求函数
      async getList(params) {
        // params是从组件接收的，包含分页和搜索字段
        const { data } = await getStockList(params)
        state.currentMarket = params.market
        // 必须要返回一个对象，包含data数组和total总数
        return { data: data.list, total: data.total }
      },
      // 【查看数据)】按钮
      pageShow: 'stock-list',
      row: {},
      async btnViewData(row) {
        state.pageShow = 'view-data'
        state.row = row
      },
      // 当前的证券交易所,默认1：深市
      currentMarket: 1,
    })
    const table = ref(null)
    const refresh = () => {
      table.value.refresh()
    }
    return {
      ...toRefs(state),
      refresh,
      table,
    }
  },
})
</script>
<style></style>
