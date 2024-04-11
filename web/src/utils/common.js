/*
 * @Description: 共通处理函数
 * @Date: 2024-04-06 19:05:47
 */

// 获取当前年月日（YYYY-MM-DD）格式
export function getNowFormatDate(date) {
  // let date = new Date()
  let year = date.getFullYear() //获取完整的年份(4位)
  let month = date.getMonth() + 1 //获取当前月份(0-11,0代表1月)
  let strDate = date.getDate() // 获取当前日(1-31)
  if (month < 10) month = `0${month}` // 如果月份是个位数，在前面补0
  if (strDate < 10) strDate = `0${strDate}` // 如果日是个位数，在前面补0

  return `${year}-${month}-${strDate}`
}
