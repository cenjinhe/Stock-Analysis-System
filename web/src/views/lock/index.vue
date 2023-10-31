<!--
 * 
 * 　　┏┓　　　┏┓+ +
 * 　┏┛┻━━━┛┻┓ + +
 * 　┃　　　　　　　┃ 　
 * 　┃　　　━　　　┃ ++ + + +
 *  ████━████ ┃+
 * 　┃　　　　　　　┃ +
 * 　┃　　　┻　　　┃
 * 　┃　　　　　　　┃ + +
 * 　┗━┓　　　┏━┛
 * 　　　┃　　　┃　　　　　　　　　　　
 * 　　　┃　　　┃ + + + +
 * 　　　┃　　　┃
 * 　　　┃　　　┃ +  神兽保佑
 * 　　　┃　　　┃    代码无bug　　
 * 　　　┃　　　┃　　+　　　　　　　　　
 * 　　　┃　 　　┗━━━┓ + +
 * 　　　┃ 　　　　　　　┣┓
 * 　　　┃ 　　　　　　　┏┛
 * 　　　┗┓┓┏━┳┓┏┛ + + + +
 * 　　　　┃┫┫　┃┫┫
 * 　　　　┗┻┛　┗┻┛+ + + +
 * 
 * 
 * @Description:
 * @version: 
 * @Date: 2021-04-23 15:25:51
 * @LastEditors: cenjinhe@126.com
 * @LastEditTime: 2021-04-26 11:34:26
 * @Author: cenjinhe@126.com
 * @HomePage: https://cenjinhe.gitee.io/Stock-System
 * @Github: https://github.com/cenjinhe/Stock-System
 * @Donate: https://cenjinhe.gitee.io/Stock-System/donate/
 -->

<template>
  <div class="lock-wrap">
    <Unlock />
    <Clock />
    <current-time />
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import Unlock from './Unlock.vue'
import Clock from './Clock.vue'
import CurrentTime from './CurrentTime.vue'

export default defineComponent({
  name: 'lock',
  components: {
    Unlock,
    Clock,
    CurrentTime,
  },
  setup() {},
})
</script>

<style lang="scss" scoped>
.lock-wrap {
  background: #222;
  height: 100%;
  min-height: 480px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
</style>
