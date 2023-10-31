<!--
 * @Description:
 * @version: 
 * @Date: 2021-04-20 11:06:21
 * @LastEditors: cenjinhe@126.com
 * @LastEditTime: 2021-04-28 15:27:11
 * @Author: cenjinhe@126.com
 * @HomePage: https://cenjinhe.gitee.io/Stock-System
 * @Github: https://github.com/cenjinhe/Stock-System
 * @Donate: https://cenjinhe.gitee.io/Stock-System/donate/
-->
<script>
import { h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
export default {
  setup() {
    const router = useRouter()
    const route = useRoute()
    router.replace(route.fullPath.replace(/^\/redirect/, ''))
  },
  render() {
    return h('div')
  },
}
</script>
