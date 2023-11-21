<template>
  <pro-table
    ref="table"
    title="拟合斜率"
    :request="getList"
    :columns="columns"
    :search="searchConfig"
    @selectionChange="handleSelectionChange"
  >
    <!-- 工具栏 -->
    <template #toolbar>
      <el-button type="primary" icon="Delete" @click="batchDelete">
        {{ $t('test/list.batchDelete') }}
      </el-button>
      <el-button type="primary" icon="Plus" @click="$router.push('/test/add')">
        {{ $t('test/list.add') }}
      </el-button>
      <el-button type="primary" icon="Refresh" @click="refresh">
        {{ $t('test/list.refresh') }}
      </el-button>
    </template>
    <template #status="{row}">
      <el-tag :type="row.status === 1 ? 'success' : 'error'">
        {{ row.status === 1 ? $t('public.enabled') : $t('public.disabled') }}
      </el-tag>
    </template>
    <template #operate="scope">
      <el-button
        size="small"
        type="primary"
        @click="$router.push(`/test/edit/${scope.row.id}`)"
      >
        {{ $t('public.edit') }}
      </el-button>
      <el-button size="small" type="danger">
        {{ $t('public.delete') }}
      </el-button>
    </template>
  </pro-table>
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from 'vue'
import { getUsers } from '@/api/test'
export default defineComponent({
  name: 'testList',
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
          label: '趋势状态',
          prop: 'trade_status',
          minWidth: 100,
          tdSlot: 'trade_status',
        },
        {
          label: '斜率',
          prop: 'status',
          minWidth: 100,
          tdSlot: 'status',
        },
        {
          label: '弧度',
          prop: 'status',
          minWidth: 100,
          tdSlot: 'status',
        },
        {
          label: '角度',
          prop: 'status',
          minWidth: 100,
          tdSlot: 'status',
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
        ],
      },
      selectedItems: [],
      batchDelete() {
        console.log(state.selectedItems)
      },
      // 选择
      handleSelectionChange(arr) {
        state.selectedItems = arr
      },
      // 请求函数
      async getList(params) {
        console.log(params)
        // params是从组件接收的，包含分页和搜索字段。
        // const { data } = await getUsers(params)
        const data = { list: [], total: 0 }
        // 必须要返回一个对象，包含data数组和total总数
        return {
          data: data.list,
          total: +data.total,
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
