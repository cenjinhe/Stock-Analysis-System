<template>
  <div style="padding: 0 2px 0 2px;">
    <h2 style="line-height: 40px;">EMA 指数平滑移动平均线</h2>
    <el-input v-model="content" type="textarea" rows="20" />
    <span>说明：取n日数据的平均值作为均线</span>
</template>

<script>
export default {
  name: 'MACD',
  data() {
    return {
      content:
        '  // 计算EMA指数平滑移动平均线，用于MACD\n' +
        '  function calculateEMA(n, data, field) {\n' +
        '    let i, l, ema, a\n' +
        '    a = 2 / (n + 1)\n' +
        '    if (field) {\n' +
        '      //二维数组\n' +
        '      ema = [data[0][field]]\n' +
        '      for (i = 1, l = data.length; i < l; i++) {\n' +
        '        ema.push((a * data[i][field] + (1 - a) * ema[i - 1]).toFixed(3))\n' +
        '      }\n' +
        '    } else {\n' +
        '      //普通一维数组\n' +
        '      ema = [data[0]]\n' +
        '      for (i = 1, l = data.length; i < l; i++) {\n' +
        '        ema.push((a * data[i] + (1 - a) * ema[i - 1]).toFixed(3))\n' +
        '      }\n' +
        '    }\n' +
        '    return ema\n' +
        '  }',
    }
  },
  mounted() {},
  methods: {},
}
</script>

<style scoped></style>
