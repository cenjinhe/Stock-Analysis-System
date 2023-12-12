import Vue from 'vue'

// loading�����þֲ�ˢ�£�������������ɺ�ر�loading��
let loading
let needLoadingRequestCount = 0 // ����һ���������ڴ洢�������

function startLoading(targetdq) {
  loading = Vue.prototype.$loading({
    lock: true,
    text: 'Ŭ�������У����Ժ�...',
    background: 'rgba(255,255,255,.4)',
    spinner: 'el-icon-loading',
    target: document.querySelector(targetdq), // ���ü��ض�������
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

// ���÷���
// import {showFullScreenLoading, hideFullScreenLoading} from "@/util/loading"
//
// showFullScreenLoading('.con_r')//�������أ�ע����ڵ����class,����<div class="con_r"></div>
// hideFullScreenLoading()//�رռ���
