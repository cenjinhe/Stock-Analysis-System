<template>
  <div>
    <div style="text-align: center;">
      <el-button size="small" type="primary" icon="Back" style="float: left;" @click="btnReturn">返回</el-button>
      <el-select v-model="dataCount" value-key="id" style="float: right;padding-right: 5%;" @change="initKLine">
        <el-option v-for="item in dataOptions" :key="item.id" :label="item.label" :value="item.value"/>
      </el-select>
    </div><br />
    <!--面板组展示-->
    <div style="padding-right: 5%;margin-top: 30px;">
      <panel-group :code="row.code" @handleSetLineChartData1="handleSetLineChartData" />
    </div>
    <!--k线图-->
    <div id="main" style="margin-top: 30px;width: 100%; height: 600px;float: left;"></div>
    <!--乾坤六道法-->
    <div style="margin-top: 50px;height: 600px;">
      <h1 style="font-weight: bold;color: #303133;">乾坤六道法</h1>
      <pro-table
        ref="table"
        style="padding-left: 5%;padding-right: 5%;height: 600px"
        :request="getList"
        :columns="columns"
        :default-sort="{ prop: 'code', order: 'ascending' }"
      ></pro-table>
    </div>
  </div>
</template>

<script setup>
import { defineEmits, defineProps, onMounted, ref } from 'vue'
import PanelGroup from './PanelGroup.vue'
import { getRawDataList } from '@/api/stock-manage'
import * as echarts from 'echarts'
import { calculateMA } from '@/utils/ma'
import { calculateMACD } from '@/utils/macd'

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

// input框-获取n条历史数据
const dataCount = ref(200)
const dataOptions = ref([
  { id: 1, label: '200条历史数据', value: 200 },
  { id: 2, label: '400条历史数据', value: 400 },
  { id: 3, label: '600条历史数据', value: 600 },
  { id: 4, label: '800条历史数据', value: 800 },
  { id: 5, label: '所有历史数据', value: 0 },
])

// 初始化
onMounted(() => {
  initKLine()
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
    '#c23531', // MA5
    '#2f4554', // MA10
    '#61a0a8', // MA15
    '#d48265', // MA20
    '#91c7ae', // MA30
    '#749f83', // 成交量
    '#ca8622', // MACD
    '#bda29a', // DIFF
    '#6e7074', // DEA
    '#546570',
  ]

  // 分割原始数据
  function splitData(rawData) {
    const categoryData = []
    const values = []
    const volumes = []
    for (let i = 0; i < rawData.length; i++) {
      categoryData.push(rawData[i].splice(0, 1)[0])
      values.push(rawData[i])
      // 成交量数据
      volumes.push([i, rawData[i][4], rawData[i][0] > rawData[i][1] ? 1 : -1])
    }
    return {
      categoryData: categoryData,
      values: values,
      volumes: volumes,
    }
  }

  // 计算滑块开始位置
  function startCount() {
    const base = 60
    let len = data.values.length
    return len > base ? Math.round(((len - base) / len) * 100) : base
  }

  //=================================================
  // 获取原始数据
  // 数据意义：日期(date)，开盘(open)，收盘(close)，最低(low)，最高(high)，成交量(volume)
  const { rawData } = await getRawDataList({ count: dataCount.value, code: props.row.code })
  // 分割原始数据: x轴日期(categoryData), K线数据(values), 成交量数据(volumes)
  let data = splitData(rawData.reverse())
  // 计算 MACD 指标
  // let macdObj = calculateMACD(12, 26, 9, data.values, 1)
  let macdObj = calculateMACD(10, 21, 9, data.values, 1)
  // 配置ECharts option
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
      data: [
        '日K',
        'MA5',
        'MA10',
        'MA15',
        'MA20',
        'MA30',
        '成交量',
        'MACD',
        'DIFF',
        'DEA',
      ],
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
      seriesIndex: [6],
      // dimension: 指定用数据的『哪个维度』，映射到视觉元素上。『数据』即 series.data。
      // 可以把 series.data 理解成一个二维数组,其中每个列是一个维度,默认取 data 中最后一个维度
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
      {
        id: 'gd_kline',
        left: '8%',
        right: '6%',
        top: '10%',
        height: '200px', //日K线的高度
      },
      {
        id: 'gd_volume',
        left: '8%',
        right: '6%',
        bottom: '30%',
        height: '100px', //成交量的高度
      },
      {
        id: 'gd_macd',
        left: '8%',
        right: '6%',
        bottom: '10%',
        height: '100px', // MACD的高度
      },
    ],
    // x轴
    xAxis: [
      {
        // 坐标轴类型:'value' 数值轴，适用于连续数据。 'category' 类目轴，适用于离散的类目数据，为该类型时必须通过 data 设置类目数据。
        // 'time' 时间轴，适用于连续的时序数据， 'log' 对数轴。适用于对数数据。
        type: 'category',
        data: data.categoryData,
        scale: true,
        boundaryGap: true, // 刻度离纵轴有无间隙，默认true有间距
        axisLine: { onZero: false },
        axisLabel: { show: true }, // 显示label
        splitLine: { show: false }, // 隐藏网格线
      },
      {
        // 成交量
        type: 'category',
        gridIndex: 1,
        data: data.categoryData,
        boundaryGap: false,
        axisLine: { onZero: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false },
      },
      {
        // MACD
        type: 'category',
        gridIndex: 2,
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
      {
        // k线
        // 坐标轴类型：'value'，默认数值轴，适用于连续数据，'category'，类目轴，适用于离散的类目数据。
        // 'time'，时间轴，适用于连续的时序数据，'log'，对数轴。适用于对数数据
        type: 'value',
        inverse: false, // 是否是反向坐标轴
        scale: true,
      },
      {
        name: '成交量',
        nameTextStyle: {
          color: '#000',
          fontSize: 12,
          padding: [0, 0, -115, -90], // 上右下左与原位置距离
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
      {
        name: 'MACD',
        nameTextStyle: {
          color: '#000',
          fontSize: 12,
          padding: [0, 0, -115, -90], // 上右下左与原位置距离
        },
        nameRotate: 0, // y轴name旋转90度 使其垂直
        // nameGap: 30, // y轴name与横纵坐标轴线的间距
        // nameLocation: 'center', // y轴name处于y轴的什么位置
        scale: true,
        gridIndex: 2,
        // splitNumber: 2,
        axisLabel: { show: false }, // 是否显示刻度标签
        axisLine: { show: false }, // 是否显示分隔线。默认数值轴显示，类目轴不显示
        axisTick: { show: false },
        splitLine: { show: false },
      },
    ],
    // 背景se
    // backgroundColor: '#b8b886',
    // 滑动块组件
    dataZoom: [
      {
        type: 'inside', // 内置在坐标系中,在坐标系中滑动拖拽进行数据区域平移。
        xAxisIndex: [0, 1, 2],
        start: startCount(), // 滑动块start位置百分比
        end: 100, // 滑动块end位置百分比
      },
      {
        show: true, // 显示滑动
        xAxisIndex: [0, 1, 2], // 控件联动
        type: 'slider', // slider表示有滑动块的
        bottom: '1%', // dataZoom-slider组件离容器上侧的距离
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
          tooltip: {
            formatter: function(param) {
              return param.name + '<br>' + (param.data.coord || '')
            },
          },
        },
        // markLine: 图表标线
        markLine: {
          symbol: ['none', 'none'], // 线段两端的图表,默认开始是圆圈,结束是箭头
        },
      },
      {
        name: 'MA5', ///周均线
        type: 'line',
        data: calculateMA(5, data.values),
        smooth: true, // 是否平滑曲线显示
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: 'MA10', ///两周均线
        type: 'line',
        data: calculateMA(10, data.values),
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: 'MA15', ///三周均线
        type: 'line',
        data: calculateMA(15, data.values),
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: 'MA20', ///四周均线
        type: 'line',
        data: calculateMA(20, data.values),
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: 'MA30', ///月均线
        type: 'line',
        data: calculateMA(30, data.values),
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: '成交量',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: data.volumes,
      },
      {
        name: 'MACD',
        type: 'bar',
        xAxisIndex: 2,
        yAxisIndex: 2,
        data: macdObj.macdData,
        itemStyle: {
          normal: {
            color: function(params) {
              let colorList
              if (params.data >= 0) {
                colorList = upColor
              } else {
                colorList = downColor
              }
              return colorList
            },
          },
        },
      },
      {
        name: 'DIFF',
        type: 'line',
        xAxisIndex: 2,
        yAxisIndex: 2,
        showSymbol: false,
        data: macdObj.diffData,
        // itemStyle: {
        //   color: '#FFC069',
        // },
      },
      {
        name: 'DEA',
        type: 'line',
        xAxisIndex: 2,
        yAxisIndex: 2,
        showSymbol: false,
        data: macdObj.deaData,
        // itemStyle: {
        //   color: '#722ED1',
        // },
      },
    ],
  }
  // 初始化ECharts实例
  const myChart = echarts.init(document.getElementById('main'))
  // 使用刚指定的配置项和数据显示图表。
  if (option && typeof option === 'object') {
    myChart.setOption(option, true)
  }
  // 随着屏幕大小调节ECharts图表
  window.addEventListener('resize', () => {
    myChart.resize()
  })
}

// 点击panel的时间
function handleSetLineChartData(type) {}

// 请求函数
async function getList(params) {
  // params是从组件接收的，包含分页和搜索字段。
  // const { data } = await getStockList(params)
  // 必须要返回一个对象，包含data数组和total总数
  return { data: [], total: 0 }
}
// eslint-disable-next-line no-unused-vars
const columns = [
  { type: 'selection', width: 56 },
  {
    label: '日期',
    prop: 'id',
    minWidth: 80,
  },
  {
    label: 'MNCD',
    prop: 'code',
    minWidth: 160,
  },
  {
    label: 'KDJ',
    prop: 'name',
    minWidth: 160,
  },
  {
    label: 'RSI',
    prop: 'listing_date',
    minWidth: 160,
  },
  {
    label: 'LWR',
    prop: 'date',
    minWidth: 160,
  },
  {
    label: 'BBI',
    prop: 'pre_close',
    minWidth: 100,
  },
  {
    label: 'MTM',
    width: 180,
    align: 'center',
    tdSlot: 'operate', // 自定义单元格内容的插槽名称
  },
]
</script>

<style scoped></style>
