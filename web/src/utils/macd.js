/*
 * @Description: ���� MACD ָ��
 * @Date: 2024-01-07 19:05:47
 */

/*
 * ����EMAָ��ƽ���ƶ�ƽ���ߣ�����MACD
 * @param {number} n short or long
 * @param {array} data ����
 * @param {number} field �����ֶ�����
 */
export function calculateEMA(n, data, field) {
  let i, l, ema, a
  a = 2 / (n + 1)
  if (field) {
    //��ά����
    ema = [data[0][field]]
    for (i = 1, l = data.length; i < l; i++) {
      ema.push((a * data[i][field] + (1 - a) * ema[i - 1]).toFixed(3))
    }
  } else {
    //��ͨһά����
    ema = [data[0]]
    for (i = 1, l = data.length; i < l; i++) {
      ema.push((a * data[i] + (1 - a) * ema[i - 1]).toFixed(3))
    }
  }
  return ema
}

/*
 * ����DIF���ߣ�����MACD
 * @param {number} short  ����EMA
 * @param {number} long ����EMA
 * @param {array} data ����
 * @param {number} field �����ֶ�����
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
 * ����DEA���ߣ�����MACD
 * @param {number} mid ��dif
 * @param {array} dif ����
 */
function calculateDEA(mid, dif) {
  return calculateEMA(mid, dif)
}

/*
 * ����MACD
 * @param {number} short ����EMA
 * @param {number} long ����EMA
 * @param {number} mid deaʱ�䴰��
 * @param {array} data ����
 * @param {string} field �����ֶ�����
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
