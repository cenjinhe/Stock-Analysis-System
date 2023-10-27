<template>
  <div>
    <el-button size="small" type="primary" icon="Back" @click="btnReturn">
      返回
    </el-button>
    <div id="main" style="margin-top: 50px;width: 100%; height: 400px"></div>
  </div>
</template>

<script setup>
import { defineEmits, defineProps, onMounted } from 'vue'
import { getRawDataList } from '@/api/stock-manage'
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
  const colorList = [
    '#c23531',
    '#2f4554',
    '#61a0a8',
    '#d48265',
    '#91c7ae',
    '#749f83',
    '#ca8622',
    '#bda29a',
    '#6e7074',
    '#546570',
    '#c4ccd3',
  ]

  // 获取原始数据
  // 数据意义：开盘(open)，收盘(close)，最低(lowest)，最高(highest)
  const params = { count: 200, code: props.row.code }
  const { rawData } = await getRawDataList(params)
  let data = splitData(rawData.reverse())

  // 分割原始数据
  function splitData(rawData) {
    const categoryData = []
    const values = []
    const volumes = []
    for (let i = 0; i < rawData.length; i++) {
      categoryData.push(rawData[i].splice(0, 1)[0])
      values.push(rawData[i])
      volumes.push([i, rawData[i][4], rawData[i][0] > rawData[i][1] ? 1 : -1])
    }
    return {
      categoryData: categoryData,
      values: values,
      volumes: volumes,
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

  // 计算滑块开始位置
  function startCount() {
    const base = 60
    let len = data.values.length
    return len > base ? Math.round(((len - base) / len) * 100) : base
  }

  // ECharts option
  const option = {
    animation: true,
    color: colorList,
    // 标题
    title: {
      text: props.row.name + '(' + props.row.code + ')', // 显示名称
      left: 'left',
    },
    // 图例
    legend: {
      top: 15,
      left: 'center',
      data: ['日K', 'MA5', 'MA10', 'MA15', 'MA20', 'MA30'],
      selected: { MA30: false }, // 不需要显示的图例设置为false
    },
    // 提示框 （即鼠标移动到柱状图会显示内容）
    tooltip: {
      trigger: 'axis', // 触发类型；轴触发，axis则鼠标hover到一条柱状图显示全部数据，item则鼠标hover到折线点显示相应数据
      // axisPointer坐标轴指示器
      axisPointer: {
        type: 'cross', // 默认为line，line直线，cross十字准星，shadow阴影
        crossStyle: {
          color: '#ecc813',
        },
      },
      borderWidth: 1,
      borderColor: '#ccc',
      padding: 10,
      textStyle: {
        color: '#000',
      },
      // 提示框的位置
      position: function(pos, params, el, elRect, size) {
        const obj = { top: 50 }
        obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 150
        return obj
      },
    },
    // 工具栏
    toolbox: {},
    visualMap: {
      show: false,
      seriesIndex: 6,
      dimension: 2,
      pieces: [
        {
          value: 1,
          color: downColor,
        },
        {
          value: -1,
          color: upColor,
        },
      ],
    },
    // 图表
    grid: [
      // 图表1的配置
      {
        left: '8%', // 图表显示的间距
        right: '6%',
        height: '50%',
        width: 'auto', // grid 组件的宽度。默认自适应
      },
      // 图表2的配置
      {
        left: '8%',
        right: '6%',
        top: '70%',
        height: '16%',
        width: 'auto', // grid 组件的宽度。默认自适应
      },
    ],
    // x轴
    xAxis: [
      // 图表1的x轴配置
      {
        // 坐标轴类型:'value' 数值轴，适用于连续数据。 'category' 类目轴，适用于离散的类目数据，为该类型时必须通过 data 设置类目数据。
        // 'time' 时间轴，适用于连续的时序数据， 'log' 对数轴。适用于对数数据。
        type: 'category',
        data: data.categoryData,
        scale: true,
        boundaryGap: true, // 刻度离纵轴有无间隙，默认true有间距
        axisLine: { onZero: false },
        splitLine: { show: false }, // 隐藏网格线
      },
      // 图表2的x轴配置
      {
        type: 'category',
        gridIndex: 1,
        data: data.categoryData,
        boundaryGap: false,
        axisLine: { onZero: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false },
      },
    ],
    // y轴
    yAxis: [
      // 图表1的y轴配置
      {
        show: true, // 显示y轴
        // 坐标轴类型：'value'，默认数值轴，适用于连续数据，'category'，类目轴，适用于离散的类目数据。
        // 'time'，时间轴，适用于连续的时序数据，'log'，对数轴。适用于对数数据
        type: 'value',
        inverse: false, // 是否是反向坐标轴
        scale: true,
        splitArea: {
          // show: true, // splitArea:设置数据窗口分割区域
        },
      },
      // 图表2的y轴配置
      {
        name: '成交量',
        nameTextStyle: {
          color: '#000',
          fontSize: 12,
          padding: [0, 0, -80, -90], // 上右下左与原位置距离
        },
        nameRotate: 0, // y轴name旋转90度 使其垂直
        // nameGap: 30, // y轴name与横纵坐标轴线的间距
        // nameLocation: 'center', // y轴name处于y轴的什么位置
        scale: true,
        gridIndex: 1,
        // splitNumber: 2,
        axisLabel: { show: false }, // 是否显示刻度标签
        axisLine: { show: false }, // 是否显示分隔线。默认数值轴显示，类目轴不显示
        axisTick: { show: false },
        splitLine: { show: false },
      },
    ],
    // 滑动块组件
    dataZoom: [
      {
        type: 'inside', // 内置在坐标系中,在坐标系中滑动拖拽进行数据区域平移。
        xAxisIndex: [0, 1],
        start: startCount(), // 滑动块start位置百分比
        end: 100, // 滑动块end位置百分比
      },
      {
        show: true, // 显示滑动
        xAxisIndex: [0, 1],
        type: 'slider', // slider表示有滑动块的
        top: '90%', // dataZoom-slider组件离容器上侧的距离
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
        name: 'MA15', ///三周均线
        type: 'line',
        data: calculateMA(15),
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
      {
        name: 'Volume',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: data.volumes,
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
