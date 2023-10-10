/*
 * @Description:
 * @version:
 * @Date: 2021-04-21 09:18:32
 * @LastEditors: cenjinhe@126.com
 * @LastEditTime: 2022-09-27 15:45:36
 * @Author: cenjinhe@126.com
 * @HomePage: https://cenjinhe.gitee.io/Stock-Analysis-System
 * @Github: https://github.com/cenjinhe/Stock-Analysis-System
 * @Donate: https://cenjinhe.gitee.io/Stock-Analysis-System/donate/
 */
import { defineStore } from 'pinia'

export const useErrorlog = defineStore('errorLog', {
  state: () => ({
    logs: [],
  }),
  actions: {
    addErrorLog(log) {
      // 可以根据需要将错误上报给服务器
      // ....code.......

      this.logs.push(log)
    },
    clearErrorLog() {
      this.logs.splice(0)
    },
  },
})
