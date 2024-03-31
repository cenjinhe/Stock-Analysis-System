<template>
  <el-card shadow="never">
    <div :class="advanced ? 'search' : null">
      <el-form>
        <div :class="advanced ? null : 'fold'">
          <el-row :gutter="20">
            <el-col :md="8" :sm="24">
              <el-form-item label="规则编号">
                <el-input placeholder="请输入" />
              </el-form-item>
            </el-col>
            <el-col :md="8" :sm="24">
              <el-form-item label="使用状态">
                <el-select placeholder="请选择" style="width: 100%">
                  <el-select-option value="1">关闭</el-select-option>
                  <el-select-option value="2">运行中</el-select-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :md="8" :sm="24">
              <el-form-item label="调用次数">
                <el-input-number style="width: 100%" placeholder="请输入" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row v-if="advanced" :gutter="20">
            <el-col :md="8" :sm="24">
              <el-form-item label="更新日期">
                <el-date-picker
                  style="width: 100%"
                  placeholder="请输入更新日期"
                />
              </el-form-item>
            </el-col>
            <el-col :md="8" :sm="24">
              <el-form-item label="使用状态">
                <el-select placeholder="请选择" style="width: 100%">
                  <el-select-option value="1">关闭</el-select-option>
                  <el-select-option value="2">运行中</el-select-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :md="8" :sm="24">
              <el-form-item label="描    述">
                <el-input placeholder="请输入" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        <span style="float: right; margin-top: 3px;">
          <el-button type="primary">查询</el-button>
          <el-button style="margin-left: 8px">重置</el-button>
          <a @click="toggleAdvanced" style="margin-left: 8px">
            {{ advanced ? '收起' : '展开' }}
            <el-icon>
              <component :is="advanced ? 'ArrowUp' : 'ArrowDown'" />
            </el-icon>
          </a>
        </span>
      </el-form>
    </div>
  </el-card>
</template>

<script>
export default {
  data() {
    return {
      advanced: false, // 是否展开，默认收起
    }
  },
  methods: {
    toggleAdvanced() {
      this.advanced = !this.advanced
    },
  },
}
</script>

<style scoped>
.search {
  margin-bottom: 40px;
}
.fold {
  width: calc(100% - 216px);
  display: inline-block;
}
.operator {
  margin-bottom: 18px;
}
</style>
