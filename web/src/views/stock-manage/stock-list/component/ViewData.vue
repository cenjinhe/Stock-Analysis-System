<template>
  <div>
    <el-button size="small" type="primary" icon="Back" @click="btnReturn">
      返回
    </el-button>
    <div id="main" style="margin-top: 20px;width: 100%; height: 400px"></div>
  </div>
</template>

<script setup>
import { onMounted, defineProps, defineEmits, watch, ref, toRefs } from 'vue'
import { getRawDataList } from '@/api/stock-manage'
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
  initKLine()
  // console.log(props.row)
})
// 【返回】按钮,更新父组件pageShow
const btnReturn = () => {
  emits('update:pageShow', 'stock-list') // 此处的update亦要写
}
// 初始化ECharts实例
async function initKLine() {
  const upColor = '#ec0000'
  const upBorderColor = '#8A0000'
  const downColor = '#00da3c'
  const downBorderColor = '#008F28'

  // 获取原始数据
  // 数据意义：开盘(open)，收盘(close)，最低(lowest)，最高(highest)
  const params = { count: 200, code: props.row.code }
  const { rawData } = await getRawDataList(params)
  const data = splitData(rawData.reverse())

  // 分割原始数据
  function splitData(rawData) {
    const categoryData = []
    const values = []
    for (let i = 0; i < rawData.length; i++) {
      categoryData.push(rawData[i].splice(0, 1)[0])
      values.push(rawData[i])
    }
    return {
      categoryData: categoryData,
      values: values,
    }
  }

  // 计算均线数据
  function calculateMA(dayCount) {
    const result = []
    let len = data.values.length
    for (let i = 0; i < len; i++) {
      if (i < dayCount) {
        result.push('-')
        continue
      }
      let sum = 0
      for (let j = 0; j < dayCount; j++) {
        sum += parseFloat(data.values[i - j][1])
      }
      // 保留2位小数
      result.push((sum / dayCount).toFixed(2))
    }
    return result
  }

  // ECharts option
  const option = {
    title: {
      text: props.row.name + '(' + props.row.code + ')', // 显示名称
      left: 0,
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
      },
    },
    legend: {
      data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30'],
      selected: { MA30: false }, // 不需要显示的图例设置为false
    },
    grid: {
      left: '5%', // 图表显示的位置
      right: '5%',
      bottom: '15%',
    },
    xAxis: {
      type: 'category', //'value' 数值轴，适用于连续数据。 'category' 类目轴，适用于离散的类目数据，为该类型时必须通过 data 设置类目数据。 'time' 时间轴，适用于连续的时序数据，与数值轴相比时间轴带有时间的格式化，在刻度计算上也有所不同，例如会根据跨度的范围来决定使用月，星期，日还是小时范围的刻度。 'log' 对数轴。适用于对数数据。
      data: data.categoryData,
      scale: true,
      boundaryGap: true, // 刻度离纵轴有无间隙，默认true有间距
      axisLine: { onZero: false },
      splitLine: { show: false }, // 隐藏网格线
      // splitNumber: 20,
      // min: 'dataMin',
      // max: 'dataMax',
    },
    yAxis: {
      scale: true,
      // splitArea属性设置分割区域
      splitArea: {
        // show: true,
      },
    },
    dataZoom: [
      {
        type: 'inside',
        start: 5,
        end: 100,
      },
      {
        show: true, // 显示滑动
        type: 'slider', // slider表示有滑动块的
        top: '90%',
        start: 0, // 数据窗口范围的起始百分比
        end: 100,
      },
    ],
    series: [
      {
        name: '日K',
        type: 'candlestick', // K线图
        data: data.values,
        itemStyle: {
          color: upColor, // 阳线颜色
          color0: downColor, // 阴线颜色
          borderColor: upBorderColor, // 阳线边框颜色
          borderColor0: downBorderColor, // 阴线边框颜色
        },
        markPoint: {
          label: {
            normal: {
              formatter: function(param) {
                return param != null ? Math.round(param.value) : ''
              },
            },
          },
          // data: [
          //   {
          //     name: 'XX标点',
          //     coord: ['2013/5/31', 2300],
          //     value: 2300,
          //     itemStyle: {
          //       color: 'rgb(41,60,85)',
          //     },
          //   },
          //   {
          //     name: 'highest value',
          //     type: 'max',
          //     valueDim: 'highest',
          //   },
          //   {
          //     name: 'lowest value',
          //     type: 'min',
          //     valueDim: 'lowest',
          //   },
          //   {
          //     name: 'average value on close',
          //     type: 'average',
          //     valueDim: 'close',
          //   },
          // ],
          tooltip: {
            formatter: function(param) {
              return param.name + '<br>' + (param.data.coord || '')
            },
          },
        },
        // markLine: 图表标线
        markLine: {
          symbol: ['none', 'none'], // 线段两端的图表,默认开始是圆圈,结束是箭头
          data: [
            // [
            //   {
            //     name: 'from lowest to highest', // 标注名称,可不填,不会展示出来
            //     type: 'min',
            //     valueDim: 'lowest', // K线图的取值维度open, close, lowest, highest
            //     symbol: 'circle',
            //     symbolSize: 10,
            //     label: {
            //       show: false,
            //     },
            //     emphasis: {
            //       label: {
            //         show: false,
            //       },
            //     },
            //   },
            //   {
            //     type: 'max',
            //     valueDim: 'highest',
            //     symbol: 'circle',
            //     symbolSize: 10,
            //     label: {
            //       show: false,
            //     },
            //     emphasis: {
            //       label: {
            //         show: false,
            //       },
            //     },
            //   },
            // ],
            {
              name: 'min line on close',
              type: 'min',
              valueDim: 'close',
            },
            {
              name: 'max line on close',
              type: 'max',
              valueDim: 'close',
            },
          ],
        },
      },
      {
        name: 'MA5', ///周均线
        type: 'line',
        data: calculateMA(5),
        smooth: true, // 是否平滑曲线显示
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: 'MA10', ///两周均线
        type: 'line',
        data: calculateMA(10),
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: 'MA20', ///四周均线
        type: 'line',
        data: calculateMA(20),
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: 'MA30', ///月均线
        type: 'line',
        data: calculateMA(30),
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
    ],
  }
  // 初始化ECharts实例
  const myChart = echarts.init(document.getElementById('main'))
  // 使用刚指定的配置项和数据显示图表。
  if (option && typeof option === 'object') {
    myChart.setOption(option)
  }
  // 随着屏幕大小调节图表
  window.addEventListener('resize', () => {
    myChart.resize()
  })
}
</script>

<style scoped></style>
