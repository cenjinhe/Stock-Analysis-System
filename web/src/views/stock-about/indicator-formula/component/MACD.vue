<template>
  <div style="padding: 20px 2px 2px 2px;line-height: 25px;">
    <el-card class="box-card">
      <template #header>
        <h2>EMA 指数平滑移动平均线(= DEA)</h2>
      </template>
      <el-input v-model="content_ema" type="textarea" rows="20" />
      <span style="line-height: 50px;">
      </span>
    </el-card>
    <el-card class="box-card" style="margin-top: 20px;">
      <template #header>
        <h2>DIF 快线</h2>
      </template>
      <el-input v-model="content_dif" type="textarea" rows="12" />
      <span style="line-height: 50px;">
      </span>
    </el-card>
    <el-card class="box-card" style="margin-top: 20px;">
      <template #header>
        <h2>MACD</h2>
      </template>
      <el-input v-model="content_macd" type="textarea" rows="20" />
      <span style="line-height: 50px;">
      </span>
    </el-card>
    <div style="margin-top: 40px;">
      <h2>买入点条件：</h2>
      <span style="color: red;">
        1. DEA > DIF
        <br />
        2. MACD_当前值 > MACD_前回值
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MACD',
  data() {
    return {
      content_ema:
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
      content_dif:
        '  // 计算DIF快线，用于MACD\n' +
        '  function calculateDIF(short, long, data, field) {\n' +
        '    let i, l, dif, emaShort, emaLong\n' +
        '    dif = []\n' +
        '    emaShort = calculateEMA(short, data, field)\n' +
        '    emaLong = calculateEMA(long, data, field)\n' +
        '    for (i = 0, l = data.length; i < l; i++) {\n' +
        '      dif.push((emaShort[i] - emaLong[i]).toFixed(3))\n' +
        '    }\n' +
        '    return dif\n' +
        '  }',
      content_macd:
        '  // short: 快速EMA, long: 慢速EMA, mid: DEA, field: 字段配置\n' +
        '  // calculateMACD(12, 26, 9, data.values, 1)\n' +
        '\n' +
        '  // 计算 MACD 指标\n' +
        '  function calculateMACD(short, long, mid, data, field) {\n' +
        '    let i, l, diffData, deaData, macdData\n' +
        '    macdData = []\n' +
        '    diffData = calculateDIF(short, long, data, field)\n' +
        '    deaData = calculateDEA(mid, diffData)\n' +
        '    for (i = 0, l = data.length; i < l; i++) {\n' +
        '      macdData.push(((diffData[i] - deaData[i]) * 2).toFixed(3))\n' +
        '    }\n' +
        '\n' +
        '    return {\n' +
        '      macdData,\n' +
        '      diffData,\n' +
        '      deaData,\n' +
        '    }\n' +
        '  }',
    }
  },
  mounted() {},
  methods: {},
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.box-card {
  width: auto;
}
</style>
