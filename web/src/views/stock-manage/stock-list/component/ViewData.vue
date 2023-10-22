<template>
  <div>
    <el-button size="small" type="primary" icon="Back" @click="btnReturn">返回</el-button>
    <div id="main" style="margin-top: 20px;width: 100%; height: 400px"></div>
  </div>
</template>

<script setup>
import { onMounted, defineProps, defineEmits, watch, ref, toRefs } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'


// eslint-disable-next-line no-unused-vars
const props = defineProps({
  pageShow: {
    type: String, //接收父组件数据类型
    default: 'view-data',
    required: true, //是否必传
    validator(value) {
      // 这个值必须与下列字符串中的其中一个相匹配
      return ['stock-list', 'view-data'].includes(value)
    },
  },
  row: Object, // 子组件声明了的 props ，若父组件未传，则该值为 undefined
})
const emits = defineEmits(['update:pageShow']) // 此处需写'update'
// 初始化
onMounted(() => {
  initECharts()
  ElMessage(props.row.code)
  console.log(props.row)
})
// 【返回】按钮,更新父组件pageShow
const btnReturn = () => {
  emits('update:pageShow', 'stock-list') // 此处的update亦要写
}
// 初始化ECharts实例
function initECharts() {
  const myChart = echarts.init(document.getElementById('main'))
  // 指定图表的配置项和数据
  const option = {
    title: {
      text: 'ECharts 入门示例',
    },
    tooltip: {},
    legend: {
      data: ['销量'],
    },
    xAxis: {
      data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子'],
    },
    yAxis: {},
    series: [
      {
        name: '销量',
        type: 'bar',
        data: [5, 20, 36, 10, 10, 20],
      },
    ],
  }
  // 使用刚指定的配置项和数据显示图表。
  myChart.setOption(option)
}
</script>

<style scoped></style>
