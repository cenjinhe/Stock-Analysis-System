<template>
  <div style="padding: 0 2px 0 2px;">
    <h2 style="line-height: 40px;">MA 均线</h2>
    <el-input v-model="content" type="textarea" rows="18" />
    <span>说明：取n日数据的平均值作为均线</span>
  </div>
</template>

<script>
export default {
  name: 'MA',
  data() {
    return {
      content:
        '  // 计算 MA 均线数据\n' +
        '  function calculateMA(dayCount) {\n' +
        '    const result = []\n' +
        '    let len = data.values.length\n' +
        '    for (let i = 0; i < len; i++) {\n' +
        '      if (i < dayCount) {\n' +
        "        result.push('-')\n" +
        '        continue\n' +
        '      }\n' +
        '      let sum = 0\n' +
        '      for (let j = 0; j < dayCount; j++) {\n' +
        '        sum += parseFloat(data.values[i - j][1])\n' +
        '      }\n' +
        '      // 保留2位小数\n' +
        '      result.push((sum / dayCount).toFixed(2))\n' +
        '    }\n' +
        '    return result\n' +
        '  }',
    }
  },
  mounted() {},
  methods: {},
}
</script>

<style scoped></style>
