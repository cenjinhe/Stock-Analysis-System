<template>
  <pro-table
    ref="table"
    :title="'推荐列表'"
    :request="getList"
    :columns="columns"
    :search="searchConfig"
  >
    <!-- 工具栏 -->
    <template #toolbar>
      <el-button type="primary" icon="Upload" @click="updateData">
        更新
      </el-button>
      <el-button icon="Refresh" style="margin-right: 30px;" @click="refresh">
        刷新
      </el-button>
    </template>
  </pro-table>
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from 'vue'
import { getUsers } from '@/api/test'
import { postUpdateStockSelect } from '@/api/stock-select'

export default defineComponent({
  setup() {
    // const { proxy } = getCurrentInstance()
    const state = reactive({
      columns: [
        { type: 'selection', width: 56 },
        { label: 'test/list.index', type: 'index', width: 80 },
        {
          label: 'test/list.name',
          prop: 'nickName',
          sortable: true,
          width: 180,
        },
        {
          label: 'test/list.email',
          prop: 'userEmail',
          minWidth: 200,
        },
        {
          label: 'public.status',
          tdSlot: 'status',
          width: 180,
        },
        {
          label: 'public.operate',
          width: 180,
          align: 'center',
          tdSlot: 'operate', // �Զ��嵥Ԫ�����ݵĲ������
        },
      ],
      searchConfig: {
        labelWidth: '45px',
        inputWidth: '150px',
        fields: [
          {
            type: 'text',
            label: '名称',
            name: 'nickName',
            defaultValue: 'abc',
          },
          {
            label: '状态',
            name: 'status',
            type: 'select',
            defaultValue: 1,
            options: [
              {
                name: '已发布',
                value: 1,
              },
              {
                name: '未发布',
                value: 0,
              },
            ],
          },
        ],
      },
      // 请求函数
      async getList(params) {
        const { data } = await getUsers(params)
        return {
          data: data.list,
          total: +data.total,
        }
      },
      // 更新
      async updateData() {
        const param = {}
        await postUpdateStockSelect(param)
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
