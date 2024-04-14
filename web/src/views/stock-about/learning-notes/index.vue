<template>
  <div>
    <todo-list />
  </div>
</template>

<script>
import { defineComponent, reactive, toRefs } from 'vue'
import TodoList from '@/views/stock-about/learning-notes/components/TodoList.vue'

export default defineComponent({
  components: { TodoList },
  setup() {
    const state = reactive([
    ])
    return {
      ...toRefs(state),
    }
  },
})
</script>
