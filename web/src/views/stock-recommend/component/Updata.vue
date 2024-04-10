<template>
  <el-dialog
    title="更新推荐股票"
    v-model="dialogShow"
    width="600px"
    draggable
    :close-on-click-modal="false"
    @closed="onCancel"
  >
    <el-form :model="formData" label-width="auto">
      <el-form-item label="MACD数据:">
        <el-input-number v-model="formData.macdNum" :min="100" :max="1000" style="width: 40%;" />
        <span style="margin-left: 20px;">(件)</span>
      </el-form-item>
      <el-form-item label="MACD采集:">
        <el-checkbox-group v-model="formData.checkedMACD">
          <el-checkbox class="el-checkbox-width" v-for="macd in macdList" :key="macd" :label="macd" :value="macd">
            {{ macd }}
          </el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item label="拟合斜率数据:">
        <el-input-number v-model="formData.trendNum" :min="3" :max="1000" style="width: 40%;" />
        <span style="margin-left: 20px;">(件)</span>
      </el-form-item>
      <el-form-item label="行情日期:">
        <el-date-picker v-model="formData.date" style="width: 40%;" placeholder="请输入行情日期"/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">确 定</el-button>
        <el-button  @click="onCancel">取 消</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script setup>
import { defineProps, defineEmits, ref, computed } from 'vue'
import { postUpdateStockRecommend } from '@/api/stock-recommend'
import { ElMessage } from 'element-plus'

const props = defineProps(['dialogVisible'])
const emit = defineEmits(['closeDialog'])
// 子组件中的v-model不能直接使用父组件传的值,单向数据流的概念，防止子组件修改父组件的值,所以加计算属性把props进行计算/转换
// eslint-disable-next-line no-unused-vars
const dialogShow = computed({
  get: () => props.dialogVisible,
  set: val => emit('update:closeDialog', val),
})
const macdList = ref(['1日', '3日', '5日', '7日', '14日', '20日', '30日'])
const formData = ref({
  checkedMACD: ['1日', '3日', '5日', '7日', '14日'],
  macdNum: 200,
  trendNum: 3,
  date: new Date(),
})
// 【确定】
function onSubmit() {
  postUpdateStockRecommend(formData.value)
  emit('closeDialog', false, true)
}
// 【取消】
function onCancel() {
  emit('closeDialog', false, false)
}
</script>

<style scoped>
.el-checkbox-width {
  width: 100px;
  height: 25px;
}
</style>
