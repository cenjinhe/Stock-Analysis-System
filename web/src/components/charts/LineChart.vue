<template>
  <div id="chart" :style="{ height: height, width: width }" />
</template>

<script>
import { defineComponent, defineProps } from 'vue'
import * as echarts from 'echarts'

export default defineComponent({
  props: {
    width: {
      type: String,
      default: '100%',
    },
    height: {
      type: String,
      default: '300px',
    },
    title: {
      type: Object,
      default: function() {
        return { text: 'Stacked Line11' }
      },
    },
    xData: {
      type: Array,
      default: function() {
        return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      },
    },
  },
  setup(props, context) {
    setTimeout(() => {
      // vue3使用echars图表报错：“Initialize failed:invalid dom“
      // 原因是因为：Dom没有完成加载时，echarts.init() 就已经开始执行了，获取不到Dom，无法进行操作
      // 解决方法：给echarts.init()设置定时器，延迟此操作，代码调整如下
      initLine()
    }, 1000)
    async function initLine() {
      // 配置ECharts option
      const option = {
        title: props.title,
        tooltip: {
          trigger: 'axis',
        },
        legend: {
          data: ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine'],
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true,
        },
        toolbox: {
          feature: {
            saveAsImage: {},
          },
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: props.xData,
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            name: 'Email',
            type: 'line',
            stack: 'Total',
            data: [120, 132, 101, 134, 90, 230, 210],
          },
          {
            name: 'Union Ads',
            type: 'line',
            stack: 'Total',
            data: [220, 182, 191, 234, 290, 330, 310],
          },
          {
            name: 'Video Ads',
            type: 'line',
            stack: 'Total',
            data: [150, 232, 201, 154, 190, 330, 410],
          },
          {
            name: 'Direct',
            type: 'line',
            stack: 'Total',
            data: [320, 332, 301, 334, 390, 330, 320],
          },
          {
            name: 'Search Engine',
            type: 'line',
            stack: 'Total',
            data: [820, 932, 901, 934, 1290, 1330, 1320],
          },
        ],
      }
      // 初始化ECharts实例
      let myChart = echarts.init(document.getElementById('chart'))
      // 使用刚指定的配置项和数据显示图表。
      if (option && typeof option === 'object') {
        myChart.setOption(option)
      }
      // 随着屏幕大小调节ECharts图表
      window.addEventListener('resize', () => {
        myChart.resize()
      })
    }
  },
})
</script>

<style scoped></style>
