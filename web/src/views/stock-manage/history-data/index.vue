<template>
  <pro-table
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
      <el-button type="primary" @click="updateHistoryDataSZ">
        更新数据(深)
      </el-button>
      <el-button type="primary" disabled>
        更新数据(泸)
      </el-button>
      <el-button @click="updateStockList">
        更新列表
      </el-button>
      <el-button icon="Refresh" style="margin-right: 30px;" @click="refresh">
        刷新
      </el-button>
    </template>
    <template #trade_status="{row}">
      <el-tag :type="row.trade_status === 1 ? 'success' : 'error'">
        {{ row.trade_status === 1 ? '正常' : (row.trade_status === 2 ? '退市' : '停牌') }}
      </el-tag>
    </template>
    <template #status="{row}">
      <el-tag :type="row.status === 0 ? 'success' : 'error'">
        {{ row.status === 0 ? '已更新' : '更新中' }}
      </el-tag>
    </template>
    <template #operate="scope">
      <el-button size="small" type="primary" @click="btnUpdateData(scope.row)">
        更新数据
      </el-button>
      <el-button size="small" type="danger" @click="btnDeleteRow(scope.row, scope.$index)">
        删除
      </el-button>
      <el-button size="small" type="primary" @click="btnChangeStatus(scope.row)">
        修改状态
      </el-button>
    </template>
  </pro-table>
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getStockList,
  getStatusList,
  updateStockList,
  updateStatus,
  deleteStockRecord,
  update_history_data,
  update_history_data_sz,
} from '@/api/stock-manage'

export default defineComponent({
  name: 'HistoryData',
  created(){
    console.log('created')
  },
  setup() {
    // const { proxy } = getCurrentInstance()

    const state = reactive({
      // 表格列配置，大部分属性跟el-table-column配置一样
      columns: [
        // { type: 'selection', width: 56 },
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
          label: '现价',
          prop: 'close',
          minWidth: 100,
        },
        {
          label: '交易状态',
          prop: 'trade_status',
          minWidth: 100,
          tdSlot: 'trade_status',
        },
        {
          label: '更新状态',
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
          {
            label: '交易状态',
            name: 'trade_status',
            type: 'select',
            defaultValue: 3,
            options: [
              {
                name: '全部',
                value: 3,
              },
              {
                name: '退市',
                value: 2,
              },
              {
                name: '正常',
                value: 1,
              },
              {
                name: '停牌',
                value: 0,
              },
            ],
          },
          {
            label: '更新状态',
            name: 'status',
            type: 'select',
            defaultValue: 2,
            options: [
              {
                name: '全部',
                value: 2,
              },
              {
                name: '更新中',
                value: 1,
              },
              {
                name: '已更新',
                value: 0,
              },
            ],
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
      // 【更新列表】按钮
      async updateStockList() {
        const market = table.value.searchModel.market
        const exchange = market === 1 ? '深市' : '泸市'
        ElMessageBox.confirm(`更新${exchange}A股列表, 是否继续?`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }).then(async () => {
          const market = table.value.searchModel.market
          const param = { market: market }
          await updateStockList(param)
          refresh()
          // setTimer()
          ElMessage({ type: 'success', message: '更新成功' })
        })
      },
      // 【更新深市数据(all)】按钮
      async updateHistoryDataSZ() {
        ElMessageBox.confirm(`更新深市数据, 是否继续?`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }).then(async () => {
          const param = {}
          await update_history_data_sz(param)
        })
      },
      // 【更新数据)】按钮
      async btnUpdateData(row) {
        ElMessageBox.confirm(
          `更新A股代码${row.code}历史数据, 是否继续?`,
          '提示',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        ).then(async () => {
          const market = table.value.searchModel.market
          const param = {
            market: market,
            code: row.code,
            release_date: row.date,
          }
          const { code, message } = await update_history_data(param)
          if (code === '200') {
            refresh()
            // setTimer()
            ElMessage({ type: 'success', message: '更新成功' })
          } else if (code === '201') {
            ElMessage({ type: 'warning', message: message })
          } else {
            console.log('done')
          }
        })
      },
      // 【删除)】按钮
      async btnDeleteRow(row, index) {
        ElMessageBox.confirm(
          `这将会删除A股代码[${row.code}], 是否继续?`,
          '提示',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        ).then(async () => {
          const market = table.value.searchModel.market
          const param = { market: market, id: row.id }
          await deleteStockRecord(param)
          refresh()
          ElMessage({ type: 'success', message: '删除成功' })
        })
      },
      // 【切换状态)】按钮
      async btnChangeStatus(row) {
        ElMessageBox.confirm(
          `切换A股代码${row.code}的更新状态, 是否继续?`,
          '提示',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        ).then(async () => {
          const market = table.value.searchModel.market
          const param = { market: market, code: row.code }
          const { code } = await updateStatus(param)
          if (code === '200') {
            ElMessage({ type: 'success', message: '切换成功' })
            refresh()
          } else {
            console.log('done')
          }
        })
      },
    })
    const table = ref(null)
    const refresh = () => {
      table.value.refresh()
    }
    let timer = ref(0)
    const setTimer = () => {
      if (timer.value === 0) {
        timer.value = setInterval(async () => {
          await judgeStatus()
        }, 2000)
      }
    }
    const clearTimer = () => {
      if (timer.value !== 0) {
        timer.value = 0
      }
    }
    let status_list = ref([])
    const judgeStatus = async () => {
      // 前回状态list
      let pre_status = status_list
      // 当前状态list
      const params = {
        code: table.value.searchModel.code,
        name: table.value.searchModel.name,
        status: table.value.searchModel.status,
        market: table.value.searchModel.market,
        current: table.value.pageNum,
        pageSize: table.value.pageSize,
      }
      const { data } = await getStatusList(params)
      console.log('data=', data)
      status_list.value = data

      let refreshFlg = false
      let timerFlg = true
      if (pre_status.length === status_list.value.length) {
        for (let i = 0; i < status_list.value.length; i++) {
          // status的值是否有变化
          if (pre_status[i] != status_list.value[i] && !refreshFlg) {
            refreshFlg = true
          }
          // status的值是否有更新中的状态
          if (status_list.value[i] === 1 && timerFlg) {
            timerFlg = false
          }
        }
      }
      // 刷新table
      console.log('refreshFlg=', refreshFlg)
      if (refreshFlg) {
        table.value.refresh()
      }
      // 关闭定时器
      console.log('timerFlg=', timerFlg)
      if (!timerFlg) {
        clearTimer()
      }
    }
    return {
      ...toRefs(state),
      refresh,
      setTimer,
      clearTimer,
      judgeStatus,
      timer,
      status_list,
      table,
    }
  },
  mounted(){
    console.log('mounted')
    // setTimer()
  }
})
</script>
