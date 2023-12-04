<template>
  <div>
    <pro-table
      ref="table"
      title="用户列表"
      :request="getList"
      :columns="columns"
      :search="searchConfig"
      @selectionChange="handleSelectionChange"
    >
      <!-- 工具栏 -->
      <template #toolbar>
        <el-button type="primary" icon="Plus" style="margin-right: 30px;" @click="addUser()">
          添加用户
        </el-button>
      </template>
    </pro-table>
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="30%" draggable>
      <el-form :model="formData" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="formData.username" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="formData.password" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="formData.role" placeholder="请选择角色">
            <el-option label="管理员" value="Admin" />
            <el-option label="普通用户" value="Normal" />
            <el-option label="访客" value="Guest" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="formData.notes" type="textarea" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">添加</el-button>
          <el-button  @click="onCancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from 'vue'
import { addUserInfo } from '@/api/user'

export default defineComponent({
  setup() {
    // const { proxy } = getCurrentInstance()

    const state = reactive({
      // 表格列配置，大部分属性跟el-table-column配置一样
      columns: [
        {
          label: 'ID',
          prop: 'id',
          minWidth: 80,
        },
        {
          label: '用户名',
          prop: 'username',
          minWidth: 120,
        },
        {
          label: '角色',
          prop: 'role',
          minWidth: 120,
        },
        {
          label: '备注',
          prop: 'notes',
          minWidth: 120,
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
        inputWidth: '200px', // 必须带上单位
        fields: [
          {
            type: 'text',
            label: '用户名',
            name: 'username',
            defaultValue: '',
          },
          {
            label: '角色',
            name: 'role',
            type: 'select',
            defaultValue: 0,
            options: [
              {
                name: '全部',
                value: 0,
              },
              {
                name: '管理员',
                value: 1,
              },
              {
                name: '普通用户',
                value: 2,
              },
              {
                name: '访客',
                value: 3,
              },
            ],
          },
        ],
      },
      selectedItems: [],
      // 选择
      handleSelectionChange(arr) {
        state.selectedItems = arr
      },
      // 请求函数
      async getList(params) {
        const newParams = Object.assign(params, { count: 10 })
        // const { rawData } = await getRawDataDict(newParams)
        const data = { list: [], total: 0 }
        // 必须要返回一个对象，包含data数组和total总数
        return {
          data: data.list,
          total: data.total,
        }
      },
      // 添加or删除or编辑用户
      dialogVisible: false,
      dialogTitle: '',
      addUser() {
        state.dialogTitle = '添加用户'
        state.dialogVisible = true
      },
      deleteUser(row) {
        console.log(row)
      },
      editUser() {
        state.dialogTitle = '编辑用户'
        console.log('done')
      },
      formData: {
        username: '',
        password: '',
        role: '',
        notes: '',
      },
    })
    const table = ref(null)
    const refresh = () => {
      table.value.refresh()
    }

    const onSubmit = async () => {
      console.log(state.formData)
      await addUserInfo(state.formData)
    }
    const onCancel = () => {
      state.dialogVisible = false
    }
    return { ...toRefs(state), refresh, table, onSubmit, onCancel }
  },
})
</script>
