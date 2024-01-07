<template>
  <div style="padding: 20px 2px 2px 2px;line-height: 20px;">
    <el-card class="box-card">
      <template #header>
        <h2>MA 均线</h2>
      </template>
      <el-input v-model="content" type="textarea" rows="18" />
      <span style="line-height: 50px;">
        说明：取n日数据的平均值作为均线
      </span>
    </el-card>
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
