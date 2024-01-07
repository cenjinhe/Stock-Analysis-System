/*
 * @Description: 计算 MA 均线数据
 * @Date: 2024-01-07 19:05:47
 */

/*
 * 计算 MA 均线数据
 * @param {number} dayCount 几日的均线
 * @param {array} data 数据
 */
export function calculateMA(dayCount, data) {
  const result = []
  let len = data.length
  for (let i = 0; i < len; i++) {
    if (i < dayCount) {
      result.push('-')
      continue
    }
    let sum = 0
    for (let j = 0; j < dayCount; j++) {
      sum += parseFloat(data[i - j][1])
    }
    // 保留2位小数
    result.push((sum / dayCount).toFixed(2))
  }
  return result
}
