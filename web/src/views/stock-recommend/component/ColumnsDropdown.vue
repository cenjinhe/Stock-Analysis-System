<template>
  <div>
    <el-dropdown ref="myDropdown" trigger="click" @command="handleCommand">
      <span>
        <el-icon><Setting /></el-icon>
      </span>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item>
            <span>列名显示</span>
          </el-dropdown-item>
          <el-dropdown-item v-for="(item, index) in props.columns" :key="index" :command="item.label">
            <el-checkbox v-model="item.isShow" :label="item.label" />
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue'

// columns是从父组件传过来的数据,格式如下
// columns = [
//   {label: 'ID', isShow: true},
//   {label: 'A股代码', isShow: true},
//   {label: 'A股简称', isShow: true},
//   {label: '行情日期', isShow: true},
//   {label: '收盘价(之前)', isShow: true},
//   {label: '收盘价(对比)', isShow: true}
//   ...
// ]
const props = defineProps(['columns'])
const emit = defineEmits(['changeItem'])

const all = ref('')

// 点击菜单项触发的事件回调
function handleCommand(command) {
  // https://blog.csdn.net/FellAsleep/article/details/123511579
  emit('changeItem', command)
}
</script>

<style scoped>
</style>