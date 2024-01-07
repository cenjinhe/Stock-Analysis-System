/*
 * @Description: ���� MA ��������
 * @Date: 2024-01-07 19:05:47
 */

/*
 * ���� MA ��������
 * @param {number} dayCount ���յľ���
 * @param {array} data ����
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
    // ����2λС��
    result.push((sum / dayCount).toFixed(2))
  }
  return result
}
