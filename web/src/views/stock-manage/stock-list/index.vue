<template>
  <div>
    <keep-alive>
      <pro-table
        v-if="pageShow === 'stock-list'"
        ref="table"
        :title="$t('test/list.title')"
        :request="getList"
        :columns="columns"
        :search="searchConfig"
        :default-sort="{ prop: 'code', order: 'ascending' }"
        :cell-style="cellStyle"
        @selectionChange="handleSelectionChange"
      >
        <!-- 工具栏 -->
        <template #toolbar>
          <el-button icon="Refresh" style="margin-right: 30px;" @click="refresh">
            刷新
          </el-button>
        </template>
        <template #close="scope">
          <div :style="{color: getCloseColor(scope.row)}">{{scope.row.close}}</div>
        </template>
        <template #ratio="scope">
          <div :style="{color: getCloseColor(scope.row)}">
            {{(((scope.row.close - scope.row.pre_close) / scope.row.pre_close) * 100).toFixed(2)}}%
          </div>
        </template>
        <template #trade_status="{row}">
          <el-tag :type="row.trade_status === 1 ? 'success' : 'error'">
            {{ row.trade_status === 1 ? '正常' : '停牌' }}
          </el-tag>
        </template>
        <template #operate="scope">
          <el-button size="small" type="success" @click="btnViewData(scope.row)">
            查看指标
          </el-button>
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
import ViewData from '@/views/stock-manage/stock-list/component/ViewData.vue'

export default defineComponent({
  name: 'stockList',
  components: { ViewData },
  setup() {
    // const { proxy } = getCurrentInstance()

    const state = reactive({
      // 表格列配置，大部分属性跟el-table-column配置一样
      columns: [
        { type: 'selection', width: 56 },
        {
          label: 'ID',
          prop: 'id',
          minWidth: 80,
        },
        {
          label: 'A股代码',
          prop: 'code',
          minWidth: 160,
        },
        {
          label: 'A股简称',
          prop: 'name',
          minWidth: 160,
        },
        {
          label: '上市日期',
          prop: 'listing_date',
          minWidth: 160,
        },
        {
          label: '行情日期',
          prop: 'date',
          minWidth: 160,
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
        },
        {
          label: '涨跌幅',
          prop: 'ratio',
          minWidth: 100,
          tdSlot: 'ratio',
        },
        {
          label: '交易状态',
          prop: 'trade_status',
          minWidth: 100,
          tdSlot: 'trade_status',
        },
        {
          label: '更新时间',
          prop: 'update_time',
          minWidth: 160,
        },
        {
          label: '操作',
          width: 180,
          align: 'center',
          tdSlot: 'operate', // 自定义单元格内容的插槽名称
          fixed: 'right',
        },
      ],
      // 搜索配置
      searchConfig: {
        labelWidth: '90px', // 必须带上单位
        inputWidth: '200px', // 必须带上单位
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
            type: 'radio',
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
        ],
      },
      // 选择
      selectedItems: [],
      handleSelectionChange(arr) {
        state.selectedItems = arr
      },
      getCloseColor(row) {
        if (row.close > row.pre_close) {
          return 'red'
        } else if (row.close < row.pre_close) {
          return 'green'
        } else {
          return ''
        }
      },
      // 请求函数
      async getList(params) {
        // params是从组件接收的，包含分页和搜索字段。
        const { data } = await getStockList(params)
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
