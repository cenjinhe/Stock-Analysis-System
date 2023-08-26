<template>
  <pro-table
    ref="table"
    :title="$t('test/list.title')"
    :request="getList"
    :columns="columns"
    :search="searchConfig"
    @selectionChange="handleSelectionChange"
  >
    <!-- 工具栏 -->
    <template #toolbar>
      <el-button type="primary" icon="Refresh" @click="update_stock_sz">
        更新股票(深市)
      </el-button>
      <el-button type="primary" icon="Refresh" @click="update_stock_sh">
        更新股票(沪市)
      </el-button>
    </template>
    <template #operate="scope">
      <el-button size="small" type="primary">编辑</el-button>
      <el-button size="small" type="danger">删除</el-button>
    </template>
  </pro-table>
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from 'vue'
import { getStockList, updateStockList } from '@/api/stock-manage'
export default defineComponent({
  name: 'stockList',
  setup() {
    // const { proxy } = getCurrentInstance()

    const state = reactive({
      // 表格列配置，大部分属性跟el-table-column配置一样
      columns: [
        { type: 'selection', width: 56 },
        { label: 'test/list.index', type: 'index', width: 80 },
        {
          label: 'A股代码',
          prop: 'code',
          minWidth: 180,
        },
        {
          label: 'A股简称',
          prop: 'name',
          minWidth: 200,
        },
        {
          label: '上市日期',
          prop: 'date',
          minWidth: 180,
        },
        {
          label: '更新时间',
          prop: 'update_time',
          minWidth: 180,
        },
        {
          label: '操作',
          width: 180,
          align: 'center',
          tdSlot: 'operate', // 自定义单元格内容的插槽名称
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
            name: 'stockExchange',
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
      // 请求函数
      async getList(params) {
        // params是从组件接收的，包含分页和搜索字段。
        console.log('params=', params)
        const { data } = await getStockList(params)
        // 必须要返回一个对象，包含data数组和total总数
        return { data: data.list, total: data.total }
      },
      // 【更新股票(深市)】按钮
      async update_stock_sz() {
        const param = { stockExchange: 1 }
        updateStockList(param)
      },
      // 【更新股票(沪市)】按钮
      async update_stock_sh() {
        const param = { stockExchange: 0 }
        updateStockList(param)
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
