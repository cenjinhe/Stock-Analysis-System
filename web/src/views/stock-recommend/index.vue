<template>
  <pro-table
    ref="table"
    :title="'推荐股票'"
    :request="getList"
    :columns="columns"
    :search="searchConfig"
  >
    <!-- 工具栏 -->
    <template #toolbar>
      <el-button type="primary" @click="updateStockRecommend">
        更新数据
      </el-button>
      <el-button icon="Refresh" style="margin-right: 30px;" @click="refresh">
        刷新
      </el-button>
    </template>
  </pro-table>
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from 'vue'
import {
  getStockRecommendResults,
  postUpdateStockRecommend,
} from '@/api/stock-recommend'

export default defineComponent({
  setup() {
    // const { proxy } = getCurrentInstance()
    const state = reactive({
      columns: [
        { type: 'selection', width: 56 },
        { label: '序号', type: 'index', width: 80 },
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
          label: 'MACD(前一天)',
          prop: 'previous_macd',
          minWidth: 120,
        },
        {
          label: 'MACD(现在)',
          prop: 'current_macd',
          minWidth: 120,
        },
        {
          label: 'DIF(前一天)',
          prop: 'previous_dif',
          minWidth: 120,
        },
        {
          label: 'DIF(现在)',
          prop: 'current_dif',
          minWidth: 120,
        },
        {
          label: 'DEA(前一天)',
          prop: 'previous_dea',
          minWidth: 120,
        },
        {
          label: 'DEA(现在)',
          prop: 'current_dea',
          minWidth: 120,
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
        const param = {}
        await postUpdateStockRecommend(param)
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
