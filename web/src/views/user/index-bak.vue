<template>
  <pro-table
    ref="table"
    title="用户列表"
    :request="getList"
    :columns="columns"
    :search="searchConfig"
    @selectionChange="handleSelectionChange"
  >
    <!-- 工具栏 -->
    <template #toolbar>
      <el-button icon="Refresh" style="margin-right: 30px;">
        用户
      </el-button>
    </template>
  </pro-table>
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from 'vue'

export default defineComponent({
  setup() {
    // const { proxy } = getCurrentInstance()

    const state = reactive({
      // 表格列配置，大部分属性跟el-table-column配置一样
      columns: [
        {
          label: 'ID',
          prop: 'id',
          minWidth: 80,
        },
        {
          label: '用户名',
          prop: 'username',
          minWidth: 120,
        },
        {
          label: '角色',
          prop: 'role',
          minWidth: 120,
        },
        {
          label: '备注',
          prop: 'notes',
          minWidth: 120,
        },
        {
          label: '更新时间',
          prop: 'update_time',
          minWidth: 160,
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
            label: '用户名',
            name: 'username',
            defaultValue: '',
          },
          {
            type: 'text',
            label: '角色',
            name: 'role',
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
        const newParams = Object.assign(params, { count: 10 })
        // const { rawData } = await getRawDataDict(newParams)
        const data = { list: [], total: 0 }
        // 必须要返回一个对象，包含data数组和total总数
        return {
          data: data.list,
          total: data.total,
        }
      },
    })
    const table = ref(null)
    const refresh = () => {
      table.value.refresh()
    }

    return { ...toRefs(state), refresh, table }
  },
})
</script>
