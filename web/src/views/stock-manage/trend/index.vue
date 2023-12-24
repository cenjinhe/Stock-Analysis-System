<template>
  <pro-table
    ref="table"
    title="拟合斜率"
    :request="getList"
    :columns="columns"
    :search="searchConfig"
    :pagination="false"
    max-height="400px"
    @selectionChange="handleSelectionChange"
  >
    <!-- 工具栏 -->
    <template #toolbar>
      <el-button icon="Refresh" style="margin-right: 30px;" @click="updateData()">
        刷新
      </el-button>
    </template>
  </pro-table>
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from 'vue'
import { getUpTrendDataList, postUpdateTrendStatus } from '@/api/stock-manage'

export default defineComponent({
  setup() {
    // const { proxy } = getCurrentInstance()

    const state = reactive({
      // 表格列配置，大部分属性跟el-table-column配置一样
      columns: [
        {
          label: 'Index',
          type: 'index',
          minWidth: 80,
        },
        {
          label: '行情日期',
          prop: 'date',
          minWidth: 120,
        },
        {
          label: 'A股代码',
          prop: 'code',
          minWidth: 120,
        },
        {
          label: 'A股简称',
          prop: 'name',
          minWidth: 120,
        },
        {
          label: '现价',
          prop: 'close',
          minWidth: 100,
        },
        {
          label: '趋势',
          prop: 'trend_status',
          minWidth: 100,
        },
        {
          label: '斜率',
          prop: 'slope',
          minWidth: 100,
        },
        {
          label: '操作',
          width: 260,
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
            defaultValue: '002688',
          },
          {
            type: 'text',
            label: 'A股简称',
            name: 'name',
            defaultValue: '',
          },
        ],
      },
      selectedItems: [],
      // 选择
      handleSelectionChange(arr) {
        state.selectedItems = arr
      },
      // 请求函数
      async getList(params) {
        const newParams = Object.assign(params, { count: 7 })
        const { rawData } = await getUpTrendDataList(newParams)
        console.log('rawData=', rawData)
        const data = { list: [], total: 0 }
        // 必须要返回一个对象，包含data数组和total总数
        return {
          data: rawData,
          total: rawData.length,
        }
      },
    })
    const table = ref(null)
    const refresh = () => {
      table.value.refresh()
    }
    const updateData = () => {
      const param = { market: 1 }
      postUpdateTrendStatus(param)
    }
    return { ...toRefs(state), refresh, table, updateData }
  },
})
</script>
