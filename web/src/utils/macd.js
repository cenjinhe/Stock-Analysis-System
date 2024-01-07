/*
 * @Description: 计算 MACD 指标
 * @Date: 2024-01-07 19:05:47
 */

/*
 * 计算EMA指数平滑移动平均线，用于MACD
 * @param {number} n short or long
 * @param {array} data 数据
 * @param {number} field 计算字段配置
 */
export function calculateEMA(n, data, field) {
  let i, l, ema, a
  a = 2 / (n + 1)
  if (field) {
    //二维数组
    ema = [data[0][field]]
    for (i = 1, l = data.length; i < l; i++) {
      ema.push((a * data[i][field] + (1 - a) * ema[i - 1]).toFixed(3))
    }
  } else {
    //普通一维数组
    ema = [data[0]]
    for (i = 1, l = data.length; i < l; i++) {
      ema.push((a * data[i] + (1 - a) * ema[i - 1]).toFixed(3))
    }
  }
  return ema
}

/*
 * 计算DIF快线，用于MACD
 * @param {number} short  快速EMA
 * @param {number} long 慢速EMA
 * @param {array} data 数据
 * @param {number} field 计算字段配置
 */
export function calculateDIF(short, long, data, field) {
  let i, l, dif, emaShort, emaLong
  dif = []
  emaShort = calculateEMA(short, data, field)
  emaLong = calculateEMA(long, data, field)
  for (i = 0, l = data.length; i < l; i++) {
    dif.push((emaShort[i] - emaLong[i]).toFixed(3))
  }
  return dif
}

/*
 * 计算DEA慢线，用于MACD
 * @param {number} mid 对dif
 * @param {array} dif 数据
 */
function calculateDEA(mid, dif) {
  return calculateEMA(mid, dif)
}

/*
 * 计算MACD
 * @param {number} short 快速EMA
 * @param {number} long 慢速EMA
 * @param {number} mid dea时间窗口
 * @param {array} data 数据
 * @param {string} field 计算字段配置
 */
export function calculateMACD(short = 12, long = 26, mid = 9, data, field = 1) {
  let i, l, diffData, deaData, macdData
  macdData = []
  diffData = calculateDIF(short, long, data, field)
  deaData = calculateDEA(mid, diffData)
  for (i = 0, l = data.length; i < l; i++) {
    macdData.push(((diffData[i] - deaData[i]) * 2).toFixed(3))
  }

  return {
    macdData,
    diffData,
    deaData,
  }
}
