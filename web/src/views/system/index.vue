<template>
  <div>
    system1
  </div>
</template>

<script>
import { defineComponent, reactive, toRefs } from 'vue'

export default defineComponent({
  setup() {
    const state = reactive({
    })
    return { ...toRefs(state) }
  },
})
</script>

<style scoped>
</style>
