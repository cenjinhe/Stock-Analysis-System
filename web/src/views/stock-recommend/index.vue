<template>
  <div>
    <el-card v-if="pageShow === 'stock-list'" style="margin-bottom: 10px;" shadow="never">
      <div :class="advanced ? 'search' : null">
        <el-form :modal="formData" label-width="auto">
          <div :class="advanced ? null : 'fold'">
            <el-row :gutter="20">
              <el-col :md="8" :sm="24">
                <el-form-item label="A股代码">
                  <el-input v-model="formData.code" placeholder="A股代码" clearable style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :md="8" :sm="24">
                <el-form-item label="A股简称">
                  <el-input v-model="formData.name" placeholder="A股简称" clearable style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :md="8" :sm="24">
                <el-form-item label="MACD范围">
                  <!-- 只能输入数字，允许输入小数点和负号，且只能输入两位小数（正数、负数、0）-->
                  <el-input
                    v-model.trim="formData.macdStart"
                    maxlength="16"
                    oninput="value=value.replace(/^([0-9-]\d*\.?\d{0,2})?.*$/,'$1')"
                    style="width: 45%;"
                    @blur="formData.macdStart = $event.target.value"
                  />
                  <span style="width: 10%;text-align: center;">-</span>
                  <el-input
                    v-model.trim="formData.macdEnd"
                    maxlength="16"
                    oninput="value=value.replace(/^([0-9-]\d*\.?\d{0,2})?.*$/,'$1')"
                    style="width: 45%;"
                    @blur="formData.macdEnd = $event.target.value"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row v-if="advanced" :gutter="20">
              <el-col :md="8" :sm="24">
                <el-form-item label="对比日期">
                  <el-select v-model="formData.compareDate" placeholder="请选择" style="width: 100%">
                    <el-option label="现在的收盘价" value="0" />
                    <el-option label="5日后的收盘价" value="5" />
                    <el-option label="7日后的收盘价" value="7" />
                    <el-option label="10日后的收盘价" value="10" />
                    <el-option label="15日后的收盘价" value="15" />
                    <el-option label="30日后的收盘价" value="30" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :md="8" :sm="24">
                <el-form-item label="A股简称">
                  <el-input v-model="formData.name" placeholder="A股简称" clearable style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :md="8" :sm="24">
                <el-form-item label="A股简称">
                  <el-input v-model="formData.name" placeholder="A股简称" clearable style="width: 100%" />
                </el-form-item>
              </el-col>
            </el-row>
          </div>
          <span style="float: right; margin-top: 3px;">
            <el-button type="primary" icon="Search" @click="btn_query()">查 询</el-button>
            <el-button style="margin-left: 8px" icon="RefreshRight" @click="btn_reset()">重 置</el-button>
            <a @click="toggleAdvanced" style="margin-left: 8px">
              {{ advanced ? '收起' : '展开' }}
              <el-icon><component :is="advanced ? 'ArrowUp' : 'ArrowDown'" /></el-icon>
            </a>
          </span>
        </el-form>
      </div>
    </el-card>
    <keep-alive>
      <pro-table
        v-if="pageShow === 'stock-list'"
        ref="table"
        :title="status==='updating' ? `推荐股票 (status: ${status})` : '推荐股票'"
        :request="getList"
        :columns="columns"
        @sort-change="changeTableSort"
      >
        <!-- 工具栏 -->
        <template #toolbar>
          <el-button type="warning" :disabled="status==='updating'" @click="btn_updataDialog(true)">
            更新推荐股票
          </el-button>
          <el-button type="primary" :disabled="status==='updating'" @click="btn_updateCurrentClose()">
            更新收盘价(现在)
          </el-button>
          <el-button icon="Refresh" style="margin-right: 30px;" @click="refresh">
            刷新
          </el-button>
        </template>
        <!-- table栏 -->
        <template #current_close="scope">
          <div :style="{color: getColor(scope.row.close, scope.row.current_close)}">
            {{ scope.row.current_close }}
          </div>
        </template>
        <template #ratio="scope">
          <div :style="{color: getColor(scope.row.close, scope.row.current_close)}">{{ getRatio(scope.row) }}%</div>
        </template>
        <template #operate="scope">
          <el-button size="small" type="success" @click="btnViewData(scope.row)">
            详情
          </el-button>
          <el-button size="small" type="primary" disabled @click="btnViewData(scope.row)">
            买入
          </el-button>
        </template>
      </pro-table>
    </keep-alive>
    <view-data v-if="pageShow === 'view-data'" v-model:pageShow="pageShow" v-model:row="row" />
    <UpData
      :dialogVisible="dialogUpDataVisible.visible"
      @closeDialog="btn_updataDialog"
    ></UpData>
  </div>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus'
import { defineComponent, reactive, ref, toRefs } from 'vue'
import ViewData from '@/views/stock-list/component/ViewData.vue'
import UpData from '@/views/stock-recommend/component/Updata.vue'
import { getConfigValue } from '@/api/stock-config'
import {
  getStockRecommendResults,
  postUpdateCurrentClose,
} from '@/api/stock-recommend'

export default defineComponent({
  components: { ViewData, UpData },
  setup() {
    // const { proxy } = getCurrentInstance()
    const state = reactive({
      columns: [
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
          label: '行情日期',
          prop: 'date',
          minWidth: 120,
        },
        {
          label: '收盘价(之前)',
          prop: 'close',
          minWidth: 130,
          sortable: 'custom',
        },
        {
          label: '收盘价(现在)',
          prop: 'current_close',
          minWidth: 130,
          tdSlot: 'current_close',
          sortable: 'custom',
        },
        {
          label: '涨跌幅',
          prop: 'ratio',
          minWidth: 100,
          tdSlot: 'ratio',
        },
        {
          label: 'MACD',
          prop: 'current_macd',
          minWidth: 120,
          sortable: 'custom',
        },
        {
          label: 'DIF',
          prop: 'current_dif',
          minWidth: 120,
          sortable: 'custom',
        },
        {
          label: 'DEA',
          prop: 'current_dea',
          minWidth: 120,
          sortable: 'custom',
        },
        {
          label: 'MA_3',
          prop: 'current_ma_3',
          minWidth: 120,
          sortable: 'custom',
        },
        {
          label: 'MA_5',
          prop: 'current_ma_5',
          minWidth: 120,
          sortable: 'custom',
        },
        {
          label: '更新日期',
          prop: 'update_time',
          minWidth: 180,
        },
        {
          label: '操作',
          minWidth: 140,
          align: 'center',
          tdSlot: 'operate', // 自定义单元格内容的插槽名称
          fixed: 'right',
        },
      ],
      // 请求函数
      async getList(params = null) {
        const queryParams = params
          ? Object.assign(params, state.formData)
          : Object.assign(table.value.searchModel, state.formData)
        const { data } = await getStockRecommendResults(queryParams)
        return {
          data: data.list,
          total: +data.total,
        }
      },
      // 【查询】按钮
      async btn_query() {
        await state.getList()
        refresh()
      },
      // 【重置】按钮
      async btn_reset() {
        state.formData = {
          code: '',
          name: '',
          macdStart: -0.1,
          macdEnd: 0.1,
        }
        await state.getList()
        refresh()
      },
      // 【更新当前收盘价】按钮
      async btn_updateCurrentClose() {
        ElMessageBox.confirm(`更新当前收盘价, 是否继续?`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        })
          .then(async () => {
            postUpdateCurrentClose({})
            // 设定状态定时器
            state.setStatusTimer()
          })
          .catch(() => {})
      },
      // 【查看数据)】按钮
      pageShow: 'stock-list',
      row: {},
      async btnViewData(row) {
        state.pageShow = 'view-data'
        state.row = row
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
      // 设置颜色 上涨red, 下跌green
      getColor(value1, value2) {
        if (value2 > value1) {
          return 'red'
        } else if (value2 < value1) {
          return 'green'
        } else {
          return ''
        }
      },
      // 获取涨跌幅
      getRatio(row) {
        // 公式：100* (现在的收盘价 - 之前的收盘价) / 之前的收盘价)
        const value = 100 * ((row.current_close - row.close) / row.close)
        return value.toFixed(1)
      },
      // 查询条件栏
      advanced: true, // 是否展开，默认收起
      toggleAdvanced() {
        this.advanced = !this.advanced
      },
      formData: {
        code: '',
        name: '',
        macdStart: -0.1,
        macdEnd: 0.1,
        compareDate: '0',
      },
      // 工具栏
      timer: null,
      status: 'completed',
      dialogUpDataVisible: { visible: false },
      async btn_updataDialog(flg, isRefresh = false) {
        state.dialogUpDataVisible.visible = flg
        // 设定状态定时器
        if (isRefresh) state.setStatusTimer()
      },
      // 设定状态定时器
      setStatusTimer() {
        if (!state.timer) {
          state.timer = setInterval(async () => {
            // 获取最新状态,如果状态为completed,则清除定时器
            const { data } = await getConfigValue({ name: 'status_recommend' })
            if (data.value === 'completed') {
              clearInterval(state.timer)
              state.timer = null
            }
            if (data.value !== state.status) state.status = data.value
            refresh()
          }, 1000) // 1000毫秒，即1秒
        }
      },
    })
    const table = ref(null)
    const refresh = () => {
      table.value.refresh()
    }
    // 在组件挂载时启动定时器，更新中时页面切换，防止更新中时再执行更新
    state.setStatusTimer()
    return { ...toRefs(state), refresh, table }
  },
})
</script>
<style scoped>
.search {
  margin-bottom: 40px;
}
.fold {
  width: calc(100% - 230px);
  display: inline-block;
}
</style>
