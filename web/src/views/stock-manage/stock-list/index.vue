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
      @selectionChange="handleSelectionChange"
    >
      <!-- 工具栏 -->
      <template #toolbar>
        <el-button icon="Refresh" @click="refresh">
          刷新
        </el-button>
      </template>
      <template #operate="scope">
        <el-button size="small" type="success" @click="btnViewData">
          查看数据
        </el-button>
      </template>
    </pro-table>
    </keep-alive>
    <view-data v-if="pageShow === 'view-data'" v-model:pageShow="pageShow" />
  </div>
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from 'vue'
import { getStockList } from '@/api/stock-manage'
import ViewData from '@/views/stock-manage/stock-list/component/view-data.vue'

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
          prop: 'date',
          minWidth: 160,
        },
        {
          label: '现价',
          prop: 'close',
          minWidth: 100,
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
      // 请求函数
      async getList(params) {
        // params是从组件接收的，包含分页和搜索字段。
        const { data } = await getStockList(params)
        // 必须要返回一个对象，包含data数组和total总数
        return { data: data.list, total: data.total }
      },
      // 【查看数据)】按钮
      pageShow: 'stock-list',
      async btnViewData() {
        state.pageShow = 'view-data'
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
