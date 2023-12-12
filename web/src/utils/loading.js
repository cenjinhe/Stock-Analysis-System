import Vue from 'vue'

// loading框设置局部刷新，且所有请求完成后关闭loading框
let loading
let needLoadingRequestCount = 0 // 声明一个对象用于存储请求个数

function startLoading(targetdq) {
  loading = Vue.prototype.$loading({
    lock: true,
    text: '努力加载中，请稍候...',
    background: 'rgba(255,255,255,.4)',
    spinner: 'el-icon-loading',
    target: document.querySelector(targetdq), // 设置加载动画区域
  })
}

function endLoading() {
  loading.close()
}
export function showFullScreenLoading(targetdq) {
  if (needLoadingRequestCount === 0) {
    startLoading(targetdq)
  }
  needLoadingRequestCount++
}
export function hideFullScreenLoading() {
  if (needLoadingRequestCount <= 0) return
  needLoadingRequestCount--
  if (needLoadingRequestCount === 0) {
    endLoading()
  }
}

export default {
  showFullScreenLoading,
  hideFullScreenLoading,
}

// 调用方法
// import {showFullScreenLoading, hideFullScreenLoading} from "@/util/loading"
//
// showFullScreenLoading('.con_r')//启动加载，注意给节点添加class,例如<div class="con_r"></div>
// hideFullScreenLoading()//关闭加载
