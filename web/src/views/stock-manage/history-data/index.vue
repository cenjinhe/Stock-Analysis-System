<template>
  <div>
    <pro-table
      ref="table"
      :title="`${currentMarket === 1 ? '深市' : '沪市'}股票列表`"
      :request="getList"
      :columns="columns"
      :search="searchConfig"
      :default-sort="{ prop: 'code', order: 'ascending' }"
      @selectionChange="handleSelectionChange"
    >
      <!-- 工具栏 -->
      <template #toolbar>
        <el-button type="primary" @click="openUpdateHistoryDataDlg">
          更新数据
        </el-button>
        <el-button icon="Refresh" style="margin-right: 30px;" @click="refresh">
          刷新
        </el-button>
      </template>
      <template #trade_status="{row}">
        <el-tag :type="row.trade_status === 1 ? 'success' : 'error'">
          {{
            row.trade_status === 1
              ? '正常'
              : row.trade_status === 2
              ? '退市'
              : '停牌'
          }}
        </el-tag>
      </template>
      <template #status="{row}">
        <el-tag
          :type="row.status === 0 || row.status === false ? 'success' : 'error'"
        >
          {{ row.status === 0 || row.status === false ? '已更新' : '更新中' }}
        </el-tag>
      </template>
      <template #operate="scope">
        <el-button
          size="small"
          type="primary"
          @click="btnUpdateData(scope.row)"
        >
          更新数据
        </el-button>
        <el-button
          size="small"
          type="danger"
          @click="btnDeleteRow(scope.row, scope.$index)"
        >
          删除
        </el-button>
        <el-button
          size="small"
          type="primary"
          @click="btnChangeStatus(scope.row)"
        >
          修改状态
        </el-button>
      </template>
    </pro-table>
    <el-dialog v-model="dialogVisible" title="更新数据" width="30%" class="stock-dialog">
      <el-tabs v-model="activeName" class="stock-tabs" @tab-click="handleClick">
        <el-tab-pane label="历史数据" name="historyData">
          <el-card shadow="never">
            <el-checkbox-group v-model="checkedHistoryList">
              <el-checkbox label="更新历史数据-深市" />
              <br />
              <el-checkbox label="更新历史数据-沪市" />
            </el-checkbox-group>
          </el-card>
          <span style="margin-top: 10px;float: right">
            <el-button type="primary" @click="updateHistoryData">
              确定
            </el-button>
            <el-button @click="dialogVisible = false">取消</el-button>
          </span>
        </el-tab-pane>
        <el-tab-pane label="股票列表" name="stockList">
          <el-card shadow="never">
            <el-checkbox-group v-model="checkedStockList">
              <el-checkbox label="股票列表-深市" />
              <br />
              <el-checkbox label="股票列表-沪市" />
            </el-checkbox-group>
          </el-card>
          <span style="margin-top: 10px;float: right">
            <el-button type="primary" @click="updateStockList">
              确定
            </el-button>
            <el-button @click="dialogVisible = false">取消</el-button>
          </span>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
  </div>
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getStockList,
  updateStockList,
  updateStatus,
  deleteStockRecord,
  update_history_data_single,
  update_history_data_all,
} from '@/api/stock-manage'

const stockMap = {
  '历史数据-沪市': 0,
  '历史数据-深市': 1,
  '股票列表-沪市': 0,
  '股票列表-深市': 1,
}

export default defineComponent({
  name: 'HistoryData',
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
          minWidth: 120,
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
        state.currentMarket = params.market
        // 必须要返回一个对象，包含data数组和total总数
        return { data: data.list, total: data.total }
      },
      // open【更新数据】dialog
      async openUpdateHistoryDataDlg() {
        state.dialogVisible = true
      },
      // 【更新列表(深市or泸市)】按钮
      async updateStockList() {
        ElMessageBox.confirm(`更新股票列表, 是否继续?`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        })
          .then(async () => {
            const marketList = state.checkedStockList.map(function(n) {
              return stockMap[n]
            })
            state.dialogVisible = false
            const param = { marketList: marketList }
            await updateStockList(param)
            refresh()
            ElMessage({ type: 'success', message: '更新成功' })
          })
          .catch(() => {})
      },
      // 【更新数据(深市or泸市)】-所有股票
      async updateHistoryData() {
        ElMessageBox.confirm(`更新历史数据, 是否继续?`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        })
          .then(async () => {
            const marketList = state.checkedHistoryList.map(function(n) {
              return stockMap[n]
            })
            state.dialogVisible = false
            const param = { marketList: marketList }
            await update_history_data_all(param)
          })
          .catch(() => {})
      },
      // 【更新数据)】按钮-单个股票
      async btnUpdateData(row) {
        ElMessageBox.confirm(
          `更新A股代码${row.code}历史数据, 是否继续?`,
          '提示',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )
          .then(async () => {
            const market = table.value.searchModel.market
            const param = {
              market: market,
              code: row.code,
              release_date: row.listing_date,
            }
            setTimeout(refresh, 1500)
            const { code, message } = await update_history_data_single(param)
            if (code === '200') {
              refresh()
              ElMessage({ type: 'success', message: '更新成功' })
            } else if (code === '201') {
              ElMessage({ type: 'warning', message: message })
            } else {
              console.log('done')
            }
          })
          .catch(() => {})
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
        )
          .then(async () => {
            const market = table.value.searchModel.market
            const param = { market: market, id: row.id }
            await deleteStockRecord(param)
            refresh()
            ElMessage({ type: 'success', message: '删除成功' })
          })
          .catch(() => {})
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
        )
          .then(async () => {
            const market = table.value.searchModel.market
            const param = { market: market, code: row.code }
            const { code } = await updateStatus(param)
            if (code === '200') {
              ElMessage({ type: 'success', message: '切换成功' })
              refresh()
            } else if (code === '201') {
              ElMessage({ type: 'warning', message: '切换失败' })
            } else {
              console.log('done')
            }
          })
          .catch(() => {})
      },
      // 当前的证券交易所,默认1：深市
      currentMarket: 1,
      dialogVisible: false,
      activeName: 'historyData',
      checkedHistoryList: ['更新历史数据-深市', '更新历史数据-沪市'],
      checkedStockList: ['股票列表-深市', '股票列表-沪市'],
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
  mounted() {
    console.log('mounted')
  },
})
</script>
<style>
.stock-tabs > .el-tabs__content {
  margin-top: -20px;
  padding: 20px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
.stock-dialog > .el-dialog__body {
  padding: 0 20px;
}
</style>
