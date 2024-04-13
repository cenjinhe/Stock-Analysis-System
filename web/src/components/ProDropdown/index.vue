<template>
  <!-- 下拉有多选功能  还能输入搜索 -->
  <el-dropdown
    trigger="click"
    @visible-change="onVisibleChange"
    class="dropdown"
  >
    <span class="el-dropdown-link">
      {{ defaultTitle }}
      <el-icon class="el-icon--right"><arrow-down /></el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu :hide-on-click="false">
        <div class="drop">
          <div style="width: 100%">
            <el-input
              v-model="input"
              @input="inputEvent"
              class="input"
              size="mini"
              prefix-icon="el-icon-search"
              placeholder="搜索"
              clearable
              style="width: 100%"
            ></el-input>
          </div>
          <el-checkbox
            :indeterminate="isIndeterminate"
            v-model="checkAll"
            @change="handleCheckAllChange"
            class="checkAlls"
          >
            全选
          </el-checkbox>
          <div class="checkAllLine"></div>
          <el-checkbox-group
            v-model="isCheckIdList"
            v-if="checkboxLists.length > 0"
            @change="handleCheckedChange"
          >
            <div class="checkboxLists">
              <el-checkbox
                v-for="item in checkboxLists"
                :label="item[keys]"
                :key="item[keys]"
                style="display: block"
                class="checiboxItem"
              >
                {{ item.label }}
              </el-checkbox>
            </div>
          </el-checkbox-group>
          <div v-if="checkboxLists.length === 0" class="noData">无数据</div>
          <div class="footer">
            <el-button type="primary" plain size="mini" class="footer_close">
              关 闭
            </el-button>
            <el-button
              type="primary"
              size="mini"
              class="footer_sure"
              @click="determine"
            >
              确 定
            </el-button>
          </div>
        </div>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script>
/*
 *
 * 数据说明
 * 传进来的数据
 * checkBoxList 里面item一定有key是id，表示唯一值，label用来展示
 * checkBoxList: [{ id: "1", label: "张三", age: 5 },{ id: "2", label: "李四", age: 6 }] // 表示传进来的列表
 * defaultCheckBoxList:['1', '2', '3'] // 默认选中的值
 * keys: "id" // 表示 表示唯一值字段名称
 *
 * 向父级传值：
 * let obj = {
 *  initList, // 原始数组值
 *  initIsCheckId, // 原始id列表值
 *  isCheckIdList, // 选中的id列表值
 *  isCheckEdItem, // 选中的item列表值
 * };
 * this.$emit("checked", obj); // 把选中的信息抛出
 */

export default {
  data() {
    return {
      input: '',
      state2: '',
      checkAll: false,
      isCheckIdList: [], // 选中的
      isIndeterminate: false,
      checkboxLists: [],
      initList: [], // initList: [{ id: "1", label: "张三11", age: 5 }, { id: "2", label: "李四", age: 6 },],
      initIsCheckId: [], // 初始化id列表
    }
  },
  props: {
    defaultTitle: {
      type: String,
      default: '下拉菜单',
    },
    keys: {
      type: String,
      default: 'id', // 模拟数据 唯一值 是id
    },
    checkBoxList: {
      type: Array,
      default: function() {
        return [
          // 模拟数据 从父组件传进来的数据格式
          { id: '1', label: '张三', age: 5 },
          { id: '2', label: '李四', age: 6 },
          { id: '3', label: '王五', age: 7 },
          { id: '4', label: '赵六 ', age: 8 },
          { id: '5', label: '小英', age: 9 },
          { id: '6', label: '王麻子', age: 10 },
          { id: '7', label: '王小二', age: 11 },
          { id: '8', label: '老王', age: 12 },
          { id: '9', label: '小李', age: 13 },
        ]
      },
    },
    defaultCheckBoxList: {
      type: Array,
      default: function() {
        return ['3', '4', '5'] // 模拟数据 默认选中的id列表
      },
    },
  },

  mounted() {
    this.init()
  },

  methods: {
    init() {
      let { defaultCheckBoxList = [], checkBoxList = [] } = this
      this.initList = checkBoxList
      this.checkboxLists = this.deepClone(checkBoxList) // 深拷贝一下
      if (defaultCheckBoxList.length === 0) return
      let arr = this.getIdList()
      this.initIsCheckId = this.deepClone(arr)
      this.isCheckIdList = arr
      this.defaultCheckAllStatus()
      // 默认选中 end
    },

    // 提取id列表
    getIdList() {
      let { defaultCheckBoxList, keys = 'id' } = this
      // 默认选中 start
      let item = defaultCheckBoxList[0]
      let types = Object.prototype.toString.call(item)
      let arr = []
      // 传的是id字符串
      if (types === '[object String]') arr = defaultCheckBoxList
      // 传的是数组对象包含id
      if (types === '[object Object]')
        arr = defaultCheckBoxList.map(x => x[keys] + '')
      // 传的是id数字
      if (types === '[object Number]')
        arr = defaultCheckBoxList.map(x => x + '')
      return arr
    },

    // 确定
    determine() {
      console.log('isCheckIdList', this.isCheckIdList)
      let { keys, isCheckIdList, checkBoxList, initIsCheckId } = this
      let isCheckEdItem = checkBoxList.filter(x =>
        isCheckIdList.includes(x[keys])
      )
      let initList = this.deepClone(this.initList)
      let obj = {
        initList, // 原始数组值
        initIsCheckId, // 原始id列表值
        isCheckIdList, // 选中的id列表值
        isCheckEdItem, // 选中的itemList值
      }
      console.log('obj', obj)
      this.$emit('checked', obj) // 把选中的信息抛出
    },

    onVisibleChange(v) {
      console.log('是否展示：', v)
      if (!v) {
        // 关闭后
        let initArId = this.initIsCheckId.sort().toString()
        let isCheckIdList = this.isCheckIdList.sort().toString()
        console.log(
          '关闭dropdown,前后选项是否相同：',
          initArId === isCheckIdList
        )
        if (initArId === isCheckIdList) return // 选中的值相同 可不请求
        this.determine()
      }
    },

    // 输入事件
    inputEvent(val = '') {
      val = (val + '').toLowerCase()
      let arr = []
      if (val === '') {
        // 输入为空 把原始数组赋值
        this.checkboxLists = this.deepClone(this.initList)
      } else {
        // 有输入的内容 提取和输入的内容 匹配列表的label 相关内容
        arr = this.checkboxLists.filter(x => x.label.includes(val))
        this.checkboxLists = arr
      }
      this.defaultCheckAllStatus()
    },

    // 默认全选状态
    defaultCheckAllStatus() {
      // 选中的和原始值长度一样 全选
      this.checkAll = this.isCheckIdList.length === this.initList.length

      // 选中的大于0 并且小于原始数组长度，半选状态
      this.isIndeterminate =
        this.isCheckIdList.length > 0 &&
        this.isCheckIdList.length < this.initList.length
    },

    // 点击全选
    handleCheckAllChange(val) {
      let { keys, checkboxLists } = this
      let idList = checkboxLists.map(x => x[keys])
      this.isCheckIdList = val ? idList : []
      this.isIndeterminate = false
      //
      this.$emit('isCheckEdfn', { isCheckIdList: this.isCheckIdList })
    },

    // 点击 某一项
    handleCheckedChange(value) {
      let checkedCount = value.length
      this.checkAll = checkedCount === this.checkboxLists.length
      this.isIndeterminate =
        checkedCount > 0 && checkedCount < this.checkboxLists.length
    },

    // 深拷贝
    deepClone(source) {
      if (typeof source !== 'object' || source == null) {
        return source
      }
      const target = Array.isArray(source) ? [] : {}
      for (const key in source) {
        if (Object.prototype.hasOwnProperty.call(source, key)) {
          if (typeof source[key] === 'object' && source[key] !== null) {
            target[key] = this.deepClone(source[key])
          } else {
            target[key] = source[key]
          }
        }
      }
      return target
    },
  },
}
</script>

<style lang="scss" scoped>
.dropdown {
  cursor: pointer;
}
.drop {
  padding: 10px;
}
.input {
  width: 100px;
  margin: 0 auto;
  width: 100%;
}
.checkAlls {
  margin-top: 5px;
  padding-bottom: 5px;
  display: block;
}
.checkAllLine {
  width: 75%;
  border-bottom: 1px solid #e4e4e4;
  margin: 0 auto;
}
.checkboxLists {
  max-height: 260px;
  padding-right: 10px;
  overflow-y: scroll;
  .checiboxItem {
    margin: 3px 0;
  }
}
.noData {
  margin: 20px 0;
  font-size: 14px;
  color: #ccc;
  width: 100%;
  text-align: center;
}
.footer {
  margin-top: 15px;
  width: 100%;
  text-align: center;
  .footer_sure {
    margin-left: 20px;
  }
}
</style>
