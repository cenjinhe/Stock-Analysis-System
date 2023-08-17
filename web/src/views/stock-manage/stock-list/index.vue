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
      <el-button type="primary" icon="Refresh" @click="test">
        更新股票列表
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
import { getStockList } from '@/api/stock-manage'
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
          width: 180,
        },
        {
          label: 'A股简称',
          prop: 'name',
          minWidth: 200,
        },
        {
          label: '上市日期',
          prop: 'date',
          width: 180,
        },
        {
          label: '更新时间',
          prop: 'update_time',
          width: 180,
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
            name: 'nickName',
            defaultValue: '',
          },
          {
            type: 'text',
            label: 'A股简称',
            name: 'nickName',
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
      // 【批量删除】按钮
      batchDelete() {
        console.log(state.selectedItems)
      },
      // 选择
      selectedItems: [],
      handleSelectionChange(arr) {
        state.selectedItems = arr
      },
      // 请求函数
      async getList(params) {
        console.log(params)
        // params是从组件接收的，包含分页和搜索字段。
        const { data } = await getStockList(params)
        // const data = {
        //   list: [
        //     {
        //       code: '0001',
        //       name: '金河生物',
        //       date: '2023',
        //       update_time: '2000',
        //     },
        //     {
        //       code: '0002',
        //       name: '银河生物',
        //       date: '2001',
        //       update_time: '2023',
        //     },
        //   ],
        //   total: 2,
        // }
        // 必须要返回一个对象，包含data数组和total总数
        return {
          data: data.list,
          total: data.total,
        }
      },
    })
    const test = async () => {
      console.log('done test')
      const { data } = await getStockList()
      console.log('data=', data)
    }
    const table = ref(null)
    const refresh = () => {
      table.value.refresh()
    }

    return {
      ...toRefs(state),
      test,
      refresh,
      table,
    }
  },
})
</script>
