/*
 * @Description: ��ͨ������
 * @Date: 2024-04-06 19:05:47
 */

// ��ȡ��ǰ�����գ�YYYY-MM-DD����ʽ
export function getNowFormatDate(date) {
  // let date = new Date()
  let year = date.getFullYear() //��ȡ���������(4λ)
  let month = date.getMonth() + 1 //��ȡ��ǰ�·�(0-11,0����1��)
  let strDate = date.getDate() // ��ȡ��ǰ��(1-31)
  if (month < 10) month = `0${month}` // ����·��Ǹ�λ������ǰ�油0
  if (strDate < 10) strDate = `0${strDate}` // ������Ǹ�λ������ǰ�油0

  return `${year}-${month}-${strDate}`
}
