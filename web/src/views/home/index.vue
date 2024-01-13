<template>
  home
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from 'vue'

export default defineComponent({
  setup() {
    // const { proxy } = getCurrentInstance()

    const state = reactive({
    })
    const param = ref(null)
    return {
      ...toRefs(state),
      param,
    }
  },
})
</script>
<style></style>
