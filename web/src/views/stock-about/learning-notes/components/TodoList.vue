<template>
  <div>
    <el-card shadow="hover" style="height: auto">
      <template #header>
        <div>
          <span>待办事项</span>
          <el-button style="float: right; padding: 3px 0" text>添加</el-button>
        </div>
      </template>

      <el-table :show-header="false" :data="todoList">
        <el-table-column width="40">
          <template #default="scope">
            <el-checkbox v-model="scope.row.status" />
          </template>
        </el-table-column>
        <el-table-column>
          <template #default="scope">
            <div>
              {{ scope.row.title }}
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { defineComponent, reactive, toRefs } from 'vue'

export default defineComponent({
  setup() {
    const state = reactive([
    ])
    const todoList = [
      {
        title: '1今天要修复100个bug',
        status: false,
      },
      {
        title: '2今天要修复100个bug',
        status: false,
      },
      {
        title: '3今天要写100行代码加几个bug吧',
        status: false,
      },
      {
        title: '4今天要修复100个bug',
        status: false,
      },
      {
        title: '5今天要修复100个bug',
        status: true,
      },
      {
        title: '6今天要写100行代码加几个bug吧',
        status: true,
      },
    ]
    return {
      ...toRefs(state),
      todoList,
    }
  },
})
</script>
