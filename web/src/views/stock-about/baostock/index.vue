<!--<template>-->
<!--</template>-->

<script>
import { defineComponent, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default defineComponent({
  setup() {
    const url = ref('www.baostock.com')
    window.open(window.location.protocol + '//' + url.value, '_blank')

    // ÖØ¶¨Ïò
    // const router = useRouter()
    // const route = useRoute()
    // watch(route.path, (newPath, oldPath) => {
    //     router.push(oldPath)
    //   },{ immediate: true }
    // )
  },
})
</script>