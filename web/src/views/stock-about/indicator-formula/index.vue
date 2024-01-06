<template>
  <el-container>
    <el-aside>
      <div class="menu">
        <el-menu
          default-active="MA"
          class="el-menu-vertical-demo"
          background-color="#afc5e2"
          text-color="#fff"
          active-text-color="#409eff"
          @select="changeSidebar"
        >
          <el-menu-item index="MA">
            <template #title>1. MA均线</template>
          </el-menu-item>
          <el-menu-item index="MACD">
            <template #title>2. MACD</template>
          </el-menu-item>
        </el-menu>
      </div>
    </el-aside>
    <el-container>
      <el-header>指 标 公 式</el-header>
      <el-main>
        <!-- 仔细看，核心在这，这里是路由的出口-->
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {}
  },

  mounted() {
    // this.sidebarItem = this.$route.name
    // console.log('this.$route.name=', this.$route.name)
  },
  methods: {
    changeSidebar(newName) {
      const name = this.$route.name
      if (newName !== name) this.$router.push(newName)
    },
  },
}
</script>

<style scoped>
.menu {
  height: 800px;
  background-color: #afc5e2;
}
.el-header {
  background-color: #afc5e2;
  color: #333;
  font-size: 30px;
  text-align: center;
  line-height: 50px;
}
.el-aside {
  width: 130px;
  color: #333;
  text-align: center;
  line-height: 900px;
}

.el-main {
  background-color: #cfebe43f;
  color: #333;
  line-height: 160px;
  padding: 0 !important;
}
</style>
