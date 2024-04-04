<template>
  <div>
    <el-card v-if="pageShow === 'stock-list'" style="margin-bottom: 10px;" shadow="never">
      <div :class="advanced ? 'search' : null">
        <el-form :modal="formData" label-width="auto">
          <div :class="advanced ? null : 'fold'">
            <el-row :gutter="20">
              <el-col :md="8" :sm="24">
                <el-form-item label="ST股票">
                  <el-switch v-model="formData.hasST" active-text="包含" inactive-text="不包含"/>
                </el-form-item>
              </el-col>
              <el-col :md="8" :sm="24">
                <el-form-item label="行情日期">
                  <el-date-picker v-model="formData.date" style="width: 100%" placeholder="请输入更新日期"/>
                </el-form-item>
              </el-col>
              <el-col :md="8" :sm="24">
                <el-form-item label="5日_MACD上升">
                  <el-switch v-model="formData.fiveMACD" inline-prompt active-text="是" inactive-text="否"/>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row v-if="advanced" :gutter="20">
              <el-col :md="8" :sm="24">
                <el-form-item label="更新日期">
                  <el-date-picker v-model="formData.date" style="width: 100%" placeholder="请输入更新日期"/>
                </el-form-item>
              </el-col>
              <el-col :md="8" :sm="24">
                <el-form-item label="使用状态">
                  <el-select placeholder="请选择" style="width: 100%">
                    <el-select-option value="1">关闭</el-select-option>
                    <el-select-option value="2">运行中</el-select-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :md="8" :sm="24">
                <el-form-item label="描    述">
                  <el-input placeholder="请输入" />
                </el-form-item>
              </el-col>
            </el-row>
          </div>
          <span style="float: right; margin-top: 3px;">
            <el-button type="primary" @click="updateStockRecommend()">查询</el-button>
            <el-button style="margin-left: 8px" >重置</el-button>
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
        :title="'推荐股票'"
        :request="getList"
        :columns="columns"
        @sort-change="changeTableSort"
      >
        <!-- 工具栏 -->
        <template #toolbar>
          <el-button type="warning" @click="updataDialog(true)">
            更新推荐股票
          </el-button>
          <el-button type="primary" @click="updateCurrentClose()">
            更新当前收盘价
          </el-button>
          <el-button
            icon="Refresh"
            style="margin-right: 30px;"
            @click="refresh"
          >
            刷新
          </el-button>
        </template>
        <!-- table栏 -->
        <template #current_close="scope">
          <div
            :style="{
              color: getColor(scope.row.close, scope.row.current_close),
            }"
          >
            {{ scope.row.current_close }}
          </div>
        </template>
        <template #operate="scope">
          <el-button
            size="small"
            type="success"
            @click="btnViewData(scope.row)"
          >
            详情
          </el-button>
          <el-button
            size="small"
            type="primary"
            disabled
            @click="btnViewData(scope.row)"
          >
            买入
          </el-button>
        </template>
      </pro-table>
    </keep-alive>
    <view-data
      v-if="pageShow === 'view-data'"
      v-model:pageShow="pageShow"
      v-model:row="row"
    />
    <UpData
      :dialogVisible="dialogUpDataVisible.visible"
      @closeDialog="updataDialog"
    ></UpData>
  </div>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus'
import { defineComponent, reactive, ref, toRefs } from 'vue'
import ViewData from '@/views/stock-list/component/ViewData.vue'
import UpData from '@/views/stock-recommend/component/Updata.vue'
import {
  getStockRecommendResults,
  postUpdateStockRecommend,
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
          label: '收盘价',
          prop: 'close',
          minWidth: 100,
          sortable: 'custom',
        },
        {
          label: '当前收盘价',
          prop: 'current_close',
          minWidth: 120,
          tdSlot: 'current_close',
          sortable: 'custom',
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
          label: '操作',
          minWidth: 140,
          align: 'center',
          tdSlot: 'operate', // 自定义单元格内容的插槽名称
          fixed: 'right',
        },
      ],
      // 请求函数
      async getList(params) {
        const { data } = await getStockRecommendResults(params)
        return {
          data: data.list,
          total: +data.total,
        }
      },
      // 【更新数据】按钮
      async updateStockRecommend() {
        ElMessageBox.confirm(`更新数据, 是否继续?`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        })
          .then(async () => {
            const param = {}
            const { code, message } = await postUpdateStockRecommend(param)
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
      // 【更新当前收盘价】按钮
      async updateCurrentClose() {
        ElMessageBox.confirm(`更新当前收盘价, 是否继续?`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        })
          .then(async () => {
            const param = {}
            const { code, message } = await postUpdateCurrentClose(param)
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
      // 条件栏
      advanced: false, // 是否展开，默认收起
      toggleAdvanced() {
        this.advanced = !this.advanced
      },
      formData: {
        hasST: true,
        date: new Date(),
        fiveMACD: true,
      },
      // 工具栏
      dialogUpDataVisible: { visible: false },
      updataDialog(flg, isRefresh = false) {
        state.dialogUpDataVisible.visible = flg
        if (isRefresh) refresh()
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
<style scoped>
.search {
  margin-bottom: 40px;
}
.fold {
  width: calc(100% - 216px);
  display: inline-block;
}
.operator {
  margin-bottom: 18px;
}
</style>
