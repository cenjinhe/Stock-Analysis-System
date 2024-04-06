<template>
  <div>
    <el-card v-if="pageShow === 'stock-list'" style="margin-bottom: 10px;" shadow="never">
      <div :class="advanced ? 'search' : null">
        <el-form :modal="formData" label-width="auto">
          <div :class="advanced ? null : 'fold'">
            <el-row :gutter="20">
              <el-col :md="8" :sm="24">
                <el-form-item label="A股代码">
                  <el-input v-model="formData.code" placeholder="A股代码" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :md="8" :sm="24">
                <el-form-item label="A股简称">
                  <el-input v-model="formData.name" placeholder="A股简称" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :md="8" :sm="24">
                <el-form-item label="5日_MACD上升">
                  <el-switch v-model="formData.fiveMACD" inline-prompt active-text="是" inactive-text="否"/>
                </el-form-item>
              </el-col>
            </el-row>
<!--            <el-row v-if="advanced" :gutter="20">-->
<!--              <el-col :md="8" :sm="24">-->
<!--                <el-form-item label="更新日期">-->
<!--                  <el-date-picker v-model="formData.date" style="width: 100%" placeholder="请输入更新日期"/>-->
<!--                </el-form-item>-->
<!--              </el-col>-->
<!--              <el-col :md="8" :sm="24">-->
<!--                <el-form-item label="使用状态">-->
<!--                  <el-select placeholder="请选择" style="width: 100%">-->
<!--                    <el-select-option value="1">关闭</el-select-option>-->
<!--                    <el-select-option value="2">运行中</el-select-option>-->
<!--                  </el-select>-->
<!--                </el-form-item>-->
<!--              </el-col>-->
<!--              <el-col :md="8" :sm="24">-->
<!--                <el-form-item label="ST股票">-->
<!--                  <el-switch v-model="formData.hasST" active-text="包含" inactive-text="不包含"/>-->
<!--                </el-form-item>-->
<!--              </el-col>-->
<!--            </el-row>-->
          </div>
          <span style="float: right; margin-top: 3px;">
            <el-button type="primary" @click="btn_query()">查询</el-button>
            <el-button style="margin-left: 8px" @click="btn_reset()">重置</el-button>
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
          <el-button type="warning" @click="btn_updataDialog(true)">
            更新推荐股票
          </el-button>
          <el-button type="primary" @click="btn_updateCurrentClose()">
            更新收盘价(现在)
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
      @closeDialog="btn_updataDialog"
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
        state.formData = { code: '', name: '' }
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
        code: '',
        name: '',
      },
      // 工具栏
      dialogUpDataVisible: { visible: false },
      btn_updataDialog(flg, isRefresh = false) {
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
