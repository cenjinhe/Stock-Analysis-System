<template>
  <div class="myDiv">
    <div class="nav-left"><el-button>向左</el-button></div>
    <div class="nav-center"><el-button>居中</el-button></div>
    <div class="nav-right"><el-button>向右</el-button></div>
  </div>
</template>

<script>
export default {}
</script>

<style scoped>
.myDiv {
  padding: 10px;
  color: #fff;
  background: #3296fa;
  display: flex;       /* 设为Flex布局 */
  align-items: center; /* 子元素在竖直方向居中 */
}

.myDiv > * {
  flex: 1;             /* 子元素占满整个多余部分而不进行挤压 */
}

.myDiv .nav-left {
  display: -webkit-box;
  display: flex;
  align-items: center;
}

.myDiv .nav-center {
  flex: none;
  width: 600px;
  text-align: center;
}

.myDiv .nav-right {
  display: flex;
  align-items: center;       /* 子元素在竖直方向居中 */
  justify-content: flex-end; /*定义子元素在主轴上的对齐方式为右对齐*/
  /*text-align: right;*/
}
</style>
