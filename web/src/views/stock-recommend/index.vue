<template>
  <div>
    <keep-alive>
      <pro-table
        v-if="pageShow === 'stock-list'"
        ref="table"
        :title="'推荐股票'"
        :request="getList"
        :columns="columns"
        :search="searchConfig"
        @sort-change="changeTableSort"
      >
        <!-- 工具栏 -->
        <template #toolbar>
          <el-button type="primary" @click="updateStockRecommend">
            更新数据
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
  </div>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus'
import { defineComponent, reactive, ref, toRefs } from 'vue'
import ViewData from '@/views/stock-list/component/ViewData.vue'
import {
  getStockRecommendResults,
  postUpdateStockRecommend,
} from '@/api/stock-recommend'

export default defineComponent({
  components: { ViewData },
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
      searchConfig: {
        labelWidth: '90px',
        inputWidth: '150px',
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
    })
    const table = ref(null)
    const refresh = () => {
      table.value.refresh()
    }

    return { ...toRefs(state), refresh, table }
  },
})
</script>
<style></style>
